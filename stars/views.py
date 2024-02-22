from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):  # HttpRequest
    return HttpResponse("Hello, world. You're at the stars")


def categories(request,cat_id):  # HttpRequest
    return HttpResponse(f"<h1> Articles by category </h1><p>id: {cat_id}</p>")


def categories_by_slug(request, cat_slug):  # HttpRequest
    if request.POST:
        print(request.POST)
    return HttpResponse(f"<h1> Articles by category </h1><p>id: {cat_slug}</p>")


def archive(request, year):
    if year > 2023:
        url_redirect = reverse('cats', args=('music',))
        return redirect(url_redirect)

    return HttpResponse(f"<h1>Archive by year</h1><p >{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')
