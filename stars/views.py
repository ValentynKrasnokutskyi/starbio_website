from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  UpdateView)

from starbio import settings

from .forms import AddPostForm, ContactForm
from .models import Stars, TagPost
from .utils import DataMixin


class StarsHome(DataMixin, ListView):  # View for displaying the main page
    template_name = "stars/index.html"  # Template name
    context_object_name = "posts"  # Context variable name
    title_page = "Main page"
    cat_selected = 0

    def get_queryset(self):  # Get objects to display on the page
        s_lst = cache.get("stars_posts")
        if not s_lst:
            s_lst = Stars.published.all().select_related("cat")  # All published articles
            cache.set("stars_posts", s_lst, 15)
        return s_lst


def about(request):
    file_path = (
        "templates/content/about.txt"  # Path to the file with project information
    )
    with open(file_path, "r") as file:
        project_info = file.read()
    return render(request, "stars/about.html", {"title": "About", "project_info": project_info})


class ShowPost(DataMixin, DetailView):
    template_name = "stars/post.html"  # Template name
    slug_url_kwarg = "post_slug"  # URL parameter for getting the slug
    context_object_name = "post"  # Context variable name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context["post"])

    def get_object(self, queryset=None):  # Get the post object
        return get_object_or_404(Stars.published, slug=self.kwargs[self.slug_url_kwarg])  # Published post


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):  # View for adding a new post
    form_class = AddPostForm  # Form class
    template_name = "stars/addpage.html"  # Template name
    success_url = reverse_lazy("home")  # URL to redirect to after successful save
    title_page = "Adding an article"
    permission_required = "stars.add_stars"  # <application>.<action>_<table>

    def form_valid(self, form):
        s = form.save(commit=False)
        s.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):  # View for editing a post
    model = Stars  # Post model
    fields = ["title", "content", "photo", "is_published", "cat"]  # Editable fields
    template_name = "stars/addpage.html"  # Template name
    success_url = reverse_lazy("home")  # URL to redirect to after successful save
    title_page = "Editing an article"
    permission_required = "stars.change_stars"


class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = "stars/contact.html"
    success_url = reverse_lazy("home")
    title_page = "Feedback"

    def form_valid(self, form):
        # Receiving data from the form
        name = form.cleaned_data["name"]
        email = form.cleaned_data["email"]
        message = form.cleaned_data["content"]

        # Sending letter
        send_mail(
            "Feedback from {}".format(name),
            "Message: {}\nFrom: {}".format(message, email),
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
        )
        return super().form_valid(form)


class StarsCategory(DataMixin, ListView):  # View for displaying articles in a category
    template_name = "stars/index.html"  # Template name
    context_object_name = "posts"  # Context variable name
    allow_empty = False  # Disallow empty list

    def get_context_data(self, *, object_list=None, **kwargs):  # Additional context data
        context = super().get_context_data(**kwargs)
        cat = context["posts"][0].cat  # Get the category
        return self.get_mixin_context(context, title="Category - " + cat.name, cat_selected=cat.pk,)

    def get_queryset(self):  # Get objects to display on the page
        return Stars.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")  # Articles by category


def page_not_found(request, exception):  # View for handling 404 errors
    return HttpResponseNotFound("<h1>Page not found!!!</h1>")  # Render 404 page


class TagPostList(DataMixin, ListView):  # View for displaying articles with a specific tag
    template_name = "stars/index.html"  # Template name
    context_object_name = "posts"  # Context variable name
    allow_empty = False  # Disallow empty list

    def get_context_data(self, *, object_list=None, **kwargs):  # Additional context data
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])  # Get the tag
        return self.get_mixin_context(context, title="Tag: " + tag.tag)

    def get_queryset(self):  # Get objects to display on the page
        return Stars.published.filter(tags__slug=self.kwargs["tag_slug"]).select_related("cat")  # Articles by tag
