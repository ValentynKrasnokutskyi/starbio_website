from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .models import Stars

menu = [{'title': "About", 'url_name': 'about'},
          {'title': "Add article", 'url_name': 'add_page'},
          {'title': "Feedback", "url_name": "contact"},
          {'title': "Login", 'url_name': 'login'}
        ]

cats_db = [
    {'id': 1, 'name': 'Actors'},
    {'id': 2, 'name': 'Singers'},
    {'id': 3, 'name': 'Athletes'},
]


def index(request):  # HttpRequest
    posts = Stars.published.all()
    data = {
        'title': 'Home page',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'stars/index.html', context=data)


def about(request):
    return render(request, 'stars/about.html', {'title': 'About', 'menu': menu})


def show_post(request, post_slug):  # displaying articles by their ID
    post = get_object_or_404(Stars, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'stars/post.html', context=data)


def addpage(request):
    return HttpResponse("Adding an article")


def contact(request):
    return HttpResponse("Feedback")


def login(request):
    return HttpResponse("Authorization")


def show_category(request, cat_id):
    data = {
        'title': 'Show by category',
        'menu': menu,
        'posts': Stars.published.all(),
        'cat_selected': cat_id,
    }
    return render(request, 'stars/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')
