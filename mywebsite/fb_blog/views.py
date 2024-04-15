from django.http import HttpResponse
from django.shortcuts import render

from .models import Post

# Create your views here.
def home_view(request):
    #TODO: Flex queryset Post.objects.all()
    """Home view, returns the posts for the last three days with entries"""
    posts = Post.objects.all()
    context = {"posts":posts}
    return render(request, "fb_blog/home.html", context=context)

def detail_view(request, post_id):
    """Detail view, returns a single blogpost"""
    post = Post.objects.get(id=post_id)
    context = {"post":post}
    return render(request, "fb_blog/detail.html", context)
