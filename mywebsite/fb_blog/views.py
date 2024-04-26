from calendar import monthrange
from copy import deepcopy
from datetime import datetime, timedelta

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

from .models import BlogPost

## Logic concerning home view
def get_home_view_queryset() -> list:
    """Get the blogposts for the latest four days in the db"""
    queryset = []
    latest_dates = BlogPost.objects.values('created_at__date').distinct().order_by('-created_at__date')[:3] 
    dates = [entry['created_at__date'] for entry in latest_dates]
    for date in dates:
        queryset.append(BlogPost.objects.filter(created_at__date=date))
    return queryset


def home_view(request):
    queryset = get_home_view_queryset()
    context = {"queryset":queryset, "month_id":queryset[0][0].created_at.date()}
    return render(request, "fb_blog/home.html", context)

## Logic concerning month view
def get_number_of_days_of_month(year: int, month: int) -> int:
    """Calculates the number of days of a specific month in a specific year"""
    return monthrange(year, month)[1]


def get_year_and_month_from_month_id(month_id: str) -> list:
    """Returns year and month as int from month_id string"""
    return [int(x) for x in month_id.split("-")]

def assemble_posts(posts: list) -> list:
    """Assembles posts by the date they were created"""
    arranged_posts = []
    init_date = posts[0].created_at.date()
    sublist = []
    for post in posts:
        if post.created_at.date() == init_date:
            sublist.append(post)
            if post == posts.last():
                arranged_posts.append(sublist)
        elif post.created_at.date() != init_date:
            init_date = post.created_at.date()
            arranged_posts.append(deepcopy(sublist))
            sublist = []
            sublist.append(post)
    return arranged_posts

def get_all_posts_for_a_month(year, month) -> list:
    """Get all blogposts for a specific month"""
    return BlogPost.objects.filter(created_at__month=month, created_at__year=year)
    
def get_next_month(year, month) -> str:
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    return f"{year}-{month:02d}"

def get_previous_month(year, month) -> str:
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    return f"{year}-{month:02d}"

def month_view(request, month_id):
    year, month = get_year_and_month_from_month_id(month_id)
    all_posts_per_month = get_all_posts_for_a_month(year, month)
    if all_posts_per_month:
        queryset = assemble_posts(all_posts_per_month)
    else:
        queryset = []
    previous_month = get_previous_month(year, month)
    next_month = get_next_month(year, month)
    context = {
        "queryset":queryset, 
        "next_month":next_month,
        "previous_month":previous_month,
        }
    return render(request, "fb_blog/month.html", context)

## Logic concerning detail view
def detail_view(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    context = {"post":post}
    return render(request, "fb_blog/detail.html", context)   


## Logic concerning imprint view
def imprint_view(request):
    """Returns imprint"""
    return render(request, "fb_blog/imprint.html") 


## Logic concerning search view
def search_view(request):
    search_term = request.GET.get("q")
    if search_term:
        matching_posts = BlogPost.objects.filter(Q(body__icontains=search_term)|Q(update__icontains=search_term)|Q(title__icontains=search_term))
    else:
        matching_posts = []
    if matching_posts:
        assembled_posts = assemble_posts(matching_posts)
        context = {"queryset":assembled_posts}
    else:
        context = {"message":"No entries found"}
    return render(request, "fb_blog/search.html", context)
