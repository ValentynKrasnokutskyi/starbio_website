from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Category, Stars


# Custom filter for marital status
class MarriedFilter(admin.SimpleListFilter):
    title = "Marital status"  # Title displayed in the admin panel filter
    parameter_name = "status"  # Query parameter name for filtering

    # Define filter options and their display labels
    def lookups(self, request, model_admin):
        return [("married", "Married"), ("single", "Single"),]

    # Apply filter logic based on selected option
    def queryset(self, request, queryset):
        if self.value() == "married":
            return queryset.filter(spouse__isnull=False)
        elif self.value() == "single":
            return queryset.filter(spouse__isnull=True)


# Registering the Stars model with the admin panel
@admin.register(Stars)
class StarsAdmin(admin.ModelAdmin):
    # Define the fields to be displayed and configured in the admin interface
    fields = [
        "title",
        "slug",
        "content",
        "photo",
        "post_photo",
        "cat",
        "spouse",
        "tags",
    ]
    readonly_fields = ["post_photo"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]

    # Displayed columns in the admin list view
    list_display = ("title", "post_photo", "time_create", "is_published", "cat")

    list_display_links = ("title",)  # Make the title clickable to view details
    list_editable = ("is_published",)  # Enable editing of 'is_published' field directly from list view
    ordering = ["-time_create", "title"]  # Default ordering of records in the list view
    list_per_page = 5  # Number of records displayed per page
    actions = ["set_published", "set_draft",]  # Custom actions available in the admin interface
    search_fields = ["title__startswith", "cat__name",]  # Fields to be searched in the admin interface
    list_filter = [MarriedFilter, "cat__name", "is_published",]  # Filters displayed in the sidebar
    save_on_top = True

    # Custom method to display a brief info about the star
    @admin.display(description="Image")
    def post_photo(self, stars: Stars):
        if stars.photo:
            return mark_safe(f"<img src='{stars.photo.url}' width=50>")
        return "Without photo"

    # Custom action to publish selected posts
    @admin.action(description="Publish selected posts")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Stars.Status.PUBLISHED)
        self.message_user(request, f"{count} record(s) changed.")

    # Custom action to unpublish selected posts
    @admin.action(description="Unpublish selected posts")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Stars.Status.DRAFT)
        self.message_user(request, f"{count} post(s) have been removed from publication!", messages.WARNING,)


# Registering the Category model with the admin panel
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)  # Displayed columns in the admin list view
    list_display_links = ("id", "name",)  # Make the category name clickable to view details

# admin.site.register(Stars, StarsAdmin)  # Registering the Stars model with the admin panel
