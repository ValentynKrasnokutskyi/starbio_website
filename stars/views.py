from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Stars, Category, TagPost, UploadFiles
from .utils import DataMixin


class StarsHome(DataMixin, ListView):  # View for displaying the main page
    template_name = 'stars/index.html'  # Template name
    context_object_name = 'posts'  # Context variable name
    title_page = 'Main page'
    cat_selected = 0

    def get_queryset(self):  # Get objects to display on the page
        return Stars.published.all().select_related('cat')  # All published articles


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
                  {'title': 'About', 'form': form})


class ShowPost(DataMixin, DetailView):
    template_name = 'stars/post.html'  # Template name
    slug_url_kwarg = 'post_slug'  # URL parameter for getting the slug
    context_object_name = 'post'  # Context variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'])

    def get_object(self, queryset=None):  # Get the post object
        return get_object_or_404(Stars.published, slug=self.kwargs[self.slug_url_kwarg])  # Published post


class AddPage(DataMixin, CreateView):   # View for adding a new post
    form_class = AddPostForm   # Form class
    template_name = 'stars/addpage.html'  # Template name
    success_url = reverse_lazy('home')  # URL to redirect to after successful save
    title_page = 'Adding an article'


class UpdatePage(DataMixin, UpdateView):  # View for editing a post
    model = Stars  # Post model
    fields = ['title', 'content', 'photo', 'is_published', 'cat']  # Editable fields
    template_name = 'stars/addpage.html'  # Template name
    success_url = reverse_lazy('home')  # URL to redirect to after successful save
    title_page = 'Editing an article'


def contact(request):  # View for the contact page
    return HttpResponse("Feedback")  # Placeholder for handling feedback


def login(request):  # View for the login page
    return HttpResponse("Authorization")  # Placeholder for handling authorization


class StarsCategory(DataMixin, ListView):  # View for displaying articles in a category
    template_name = 'stars/index.html'  # Template name
    context_object_name = 'posts'  # Context variable name
    allow_empty = False  # Disallow empty list

    def get_context_data(self, *, object_list=None, **kwargs):  # Additional context data
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat  # Get the category
        return self.get_mixin_context(context,
                                      title='Category - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )

    def get_queryset(self):  # Get objects to display on the page
        return Stars.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')  # Articles by category


def page_not_found(request, exception):  # View for handling 404 errors
    return HttpResponseNotFound('<h1>Page not found</h1>')  # Render 404 page


class TagPostList(DataMixin, ListView):  # View for displaying articles with a specific tag
    template_name = 'stars/index.html'  # Template name
    context_object_name = 'posts'  # Context variable name
    allow_empty = False  # Disallow empty list

    def get_context_data(self, *, object_list=None, **kwargs):  # Additional context data
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])  # Get the tag
        return self.get_mixin_context(context, title='Tag: ' + tag.tag)

    def get_queryset(self):  # Get objects to display on the page
        return Stars.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')  # Articles by tag
