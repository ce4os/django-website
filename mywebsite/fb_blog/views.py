from calendar import monthrange
from datetime import datetime, timedelta

from django.shortcuts import render

from .models import BlogPost

def get_home_view_queryset() -> list:
    """Get the blogposts for the latest three days in the db"""
    # TODO: Refactor
    # test = BlogPost.objects.values('created_at__date').distinct()[:3]
    queryset = []
    
    latest = BlogPost.objects.latest("created_at").created_at.date()
    exclude_dates = [latest]
    scnd = BlogPost.objects.exclude(created_at__date__in=exclude_dates)[0].created_at.date()
    exclude_dates.append(scnd)
    thrd = BlogPost.objects.exclude(created_at__date__in=exclude_dates)[0].created_at.date()    
    queryset = [
        BlogPost.objects.filter(created_at__date=latest), 
        BlogPost.objects.filter(created_at__date=scnd), 
        BlogPost.objects.filter(created_at__date=thrd)
        ]
    return queryset

def home_view(request):
    #TODO: refactor
    queryset = get_home_view_queryset()
    context = {"queryset":queryset, "month_id":queryset[0][0].created_at.date()}
    return render(request, "fb_blog/home.html", context)

def get_number_of_days_of_month(year, month) -> int:
    """Calculates the number of days of a specific month in a specific year"""
    return monthrange(year, month)[1]


def get_month_view_queryset(month_id):
    #TODO: Refactor
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
    
def get_next_month(month_id):
    month = int(month_id[4:])
    year = int(month_id[:4])
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    month = str(month)
    if len(month) == 1:
        month = "0" + month
    return str(year) + month

def get_previous_month(month_id):
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

def impressum(request):
    return render(request, "fb_blog/impressum.html") 