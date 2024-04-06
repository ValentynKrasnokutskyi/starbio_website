from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .forms import AddPostForm
from .models import Stars, Category, TagPost

menu = [{'title': "About", 'url_name': 'about'},
          {'title': "Add article", 'url_name': 'add_page'},
          {'title': "Feedback", "url_name": "contact"},
          {'title': "Login", 'url_name': 'login'}
        ]


def index(request):
    data = {
        'title': 'Main page',
        'menu': menu,
        'posts': Stars.published.all().select_related('cat'),
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
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    data = {
        'title': 'Adding an article',
        'menu': menu,
        'form': form,
    }

    return render(request, 'stars/addpage.html', data)


def contact(request):
    return HttpResponse("Feedback")


def login(request):
    return HttpResponse("Authorization")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Stars.published.filter(cat_id=category.pk).select_related('cat')
    data = {
        'title': f'Category: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'stars/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Stars.Status.PUBLISHED).select_related('cat')
    data = {
        'title': f'Tag: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'stars/index.html', context=data)
