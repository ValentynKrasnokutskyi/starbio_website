from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Stars, Category, TagPost, UploadFiles

menu = [{'title': "About", 'url_name': 'about'},   # Navigation menu
          {'title': "Add article", 'url_name': 'add_page'},
          {'title': "Feedback", "url_name": "contact"},
          {'title': "Login", 'url_name': 'login'}
        ]


# def index(request):
#     data = {
#         'title': 'Main page',
#         'menu': menu,
#         'posts': Stars.published.all().select_related('cat'),
#         'cat_selected': 0,
#     }
#
#     return render(request, 'stars/index.html', context=data)


class StarsHome(ListView):  # View for displaying the main page
    template_name = 'stars/index.html'  # Template name
    context_object_name = 'posts'  # Context variable name
    extra_context = {  # Additional context data
        'title': 'Main page',  # Page title
        'menu': menu,  # Navigation menu
        'cat_selected': 0,  # Selected category (by default)
    }

    def get_queryset(self):  # Get objects to display on the page
        return Stars.published.all().select_related('cat')  # All published articles

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Main page'
    #     context['menu'] = menu
    #     context['posts'] = Stars.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context

# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #  handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'stars/about.html',
                  {'title': 'About', 'menu': menu, 'form': form})


# def show_post(request, post_slug):  # displaying articles by their ID
#     post = get_object_or_404(Stars, slug=post_slug)
#
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#     return render(request, 'stars/post.html', context=data)


class ShowPost(DetailView):
    model = Stars  # Post model
    template_name = 'stars/post.html'  # Template name
    slug_url_kwarg = 'post_slug'  # URL parameter for getting the slug
    context_object_name = 'post'  # Context variable name

    def get_context_data(self, **kwargs):  # Additional context data
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']  # Page title - post title
        context['menu'] = menu  # Navigation menu
        return context

    def get_object(self, queryset=None):  # Get the post object
        return get_object_or_404(Stars.published, slug=self.kwargs[self.slug_url_kwarg])  # Published post


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'title': 'Adding an article',
#         'menu': menu,
#         'form': form,
#     }
#
#     return render(request, 'stars/addpage.html', data)

    # def form_valid(self, form):
    #     form.save()
    #     return super().form_valid(form)


class AddPage(CreateView):   # View for adding a new post
    #  model = Stars
    #  fields = ['title', 'slug', 'content', 'is_published', 'cat']
    form_class = AddPostForm   # Form class
    template_name = 'stars/addpage.html'  # Template name
    success_url = reverse_lazy('home')  # URL to redirect to after successful save
    extra_context = {  # Additional context data
        'menu': menu,  # Navigation menu
        'title': 'Adding an article',  # Page title
    }


class UpdatePage(UpdateView):  # View for editing a post
    model = Stars  # Post model
    fields = ['title', 'content', 'photo', 'is_published', 'cat']  # Editable fields
    template_name = 'stars/addpage.html'  # Template name
    success_url = reverse_lazy('home')  # URL to redirect to after successful save
    extra_context = {  # Additional context data
        'menu': menu,  # Navigation menu
        'title': 'Edit an article',  # Page title
    }

# class AddPage(View):
#
#     def get(self, request):
#         form = AddPostForm()
#         data = {
#             'title': 'Adding an article',
#             'menu': menu,
#             'form': form,
#         }
#
#         return render(request, 'stars/addpage.html', data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#         data = {
#             'title': 'Adding an article',
#             'menu': menu,
#             'form': form,
#         }
#
#         return render(request, 'stars/addpage.html', data)


def contact(request):  # View for the contact page
    return HttpResponse("Feedback")  # Placeholder for handling feedback


def login(request):  # View for the login page
    return HttpResponse("Authorization")  # Placeholder for handling authorization


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Stars.published.filter(cat_id=category.pk).select_related('cat')
#     data = {
#         'title': f'Category: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#     return render(request, 'stars/index.html', context=data)


class StarsCategory(ListView):  # View for displaying articles in a category
    template_name = 'stars/index.html'  # Template name
    context_object_name = 'posts'  # Context variable name
    allow_empty = False  # Disallow empty list

    def get_context_data(self, *, object_list=None, **kwargs):  # Additional context data
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat  # Get the category
        context['title'] = 'Category - ' + cat.name  # Page title
        context['menu'] = menu  # Navigation menu
        context['cat_selected'] = cat.id  # Selected category
        return context

    def get_queryset(self):  # Get objects to display on the page
        return Stars.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')  # Articles by category


def page_not_found(request, exception):  # View for handling 404 errors
    return HttpResponseNotFound('<h1>Page not found</h1>')  # Render 404 page


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Stars.Status.PUBLISHED).select_related('cat')
#     data = {
#         'title': f'Tag: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'stars/index.html', context=data)


class TagPostList(ListView):  # View for displaying articles with a specific tag
    template_name = 'stars/index.html'  # Template name
    context_object_name = 'posts'  # Context variable name
    allow_empty = False  # Disallow empty list

    def get_context_data(self, *, object_list=None, **kwargs):  # Additional context data
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])  # Get the tag
        context['title'] = 'Tag: ' + tag.tag  # Page title
        context['menu'] = menu  # Navigation menu
        context['cat_selected'] = None  # No selected category
        return context

    def get_queryset(self):  # Get objects to display on the page
        return Stars.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')  # Articles by tag
