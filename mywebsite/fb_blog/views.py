from calendar import monthrange
from copy import deepcopy
from datetime import datetime, timedelta

from django.db.models import Q
from django.shortcuts import render

from .models import BlogPost

def get_home_view_queryset() -> list:
    """Get the blogposts for the latest four days in the db"""
    queryset = []
    latest_dates = BlogPost.objects.values('created_at__date').distinct().order_by('-created_at__date')[:4] 
    dates = [entry['created_at__date'] for entry in latest_dates]
    for date in dates:
        queryset.append(BlogPost.objects.filter(created_at__date=date))
    return queryset

def home_view(request):
    #TODO: refactor
    queryset = get_home_view_queryset()
    context = {"queryset":queryset, "month_id":queryset[0][0].created_at.date()}
    return render(request, "fb_blog/home.html", context)


def get_number_of_days_of_month(year: int, month: int) -> int:
    """Calculates the number of days of a specific month in a specific year"""
    return monthrange(year, month)[1]

def get_month_view_queryset(month_id: str) -> list:
    """Get all blogposts for a specific month"""
    year = int(month_id[:4])
    month = int(month_id[4:])
    days_in_month = get_number_of_days_of_month(year, month)
    last_day_of_month = datetime(year, month, days_in_month).date()
    queryset = []
    delta = timedelta(days=1)
    for i in range(0, days_in_month):
        if BlogPost.objects.filter(created_at__date=(last_day_of_month - delta*i)):
            queryset.append(BlogPost.objects.filter(created_at__date=(last_day_of_month - delta*i)))
    return queryset
    
def get_next_month(month_id: str) -> str:
    month = int(month_id[4:])
    year = int(month_id[:4])
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    return f"{year}{month:02d}"

def get_previous_month(month_id: str) -> str:
    month = int(month_id[4:])
    year = int(month_id[:4])
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    return f"{year}{month:02d}"

def month_view(request, month_id):
    queryset = get_month_view_queryset(month_id)
    previous_month = get_previous_month(month_id)
    next_month = get_next_month(month_id)
    context = {
        "queryset":queryset, 
        "next_month":next_month,
        "previous_month":previous_month,
        }
    return render(request, "fb_blog/month.html", context)


def detail_view(request, post_id):
    post = BlogPost.objects.get(pk=post_id)
    context = {"post":post}
    return render(request, "fb_blog/detail.html", context)   


def imprint_view(request):
    """Returns imprint"""
    return render(request, "fb_blog/imprint.html") 


def assemble_posts(posts: list) -> list:
    """Assembles posts by the date they were created"""
    arranged_posts = []
    init_date = posts[0].created_at.date()
    sublist = []
    for post in posts:
        if post.created_at.date() == init_date:
            sublist.append(post)
        elif post.created_at.date() != init_date:
            init_date = post.created_at.date()
            arranged_posts.append(deepcopy(sublist))
            sublist = []
            sublist.append(post)
    return arranged_posts

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