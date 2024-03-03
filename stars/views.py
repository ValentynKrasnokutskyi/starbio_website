from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

menu = [{'title': "About", 'url_name': 'about'},
          {'title': "Add article", 'url_name': 'add_page'},
          {'title': "Feedback", "url_name": "contact"},
          {'title': "Login", 'url_name': 'login'}
        ]

data_db = [
    {'id': 1, 'title': 'Angelina Jolie', 'content': '''<h1>Angelina Jolie</h1> (born Angelina Jolie[7], born Voight), formerly Jolie Pitt (born June 4, 1975, Los Angeles, California, USA) is an American film, television and voice actress, film director, screenwriter, producer, fashion model, and UN Goodwill Ambassador.
         Winner of an Oscar, three Golden Globe Awards (the first actress in history to win the award three years in a row) and two Screen Actors Guild Awards.''',
     'is_published': True},
    {'id': 2, 'title': 'Margot Robbie', 'content': 'Biography of Margot Robbie', 'is_published': False},
    {'id': 3, 'title': 'Julia Roberts', 'content': 'Biography of Julia Roberts', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Actors'},
    {'id': 2, 'name': 'Singers'},
    {'id': 3, 'name': 'Athletes'},
]


def index(request):  # HttpRequest
    data = {
        'title': 'Home page',
        'menu': menu,
        'posts': data_db,
        'cat_selected': 0,
    }
    return render(request, 'stars/index.html', context=data)


def about(request):
    return render(request, 'stars/about.html', {'title': 'About', 'menu': menu})


def show_post(request, post_id):
    return HttpResponse(f"Article show with id = {post_id}")


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
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'stars/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')
