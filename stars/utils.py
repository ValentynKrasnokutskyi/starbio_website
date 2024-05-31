# Navigation menu
menu = [
    {"title": "About", "url_name": "about"},
    {"title": "Add article", "url_name": "add_page"},
    {"title": "Feedback", "url_name": "contact"},
]


class DataMixin:
    """
    Mixin class to provide common data and functionality to views.
    """

    paginate_by = 3  # Default number of items per page
    title_page = None  # Default title for the page
    cat_selected = None  # Default selected category
    extra_context = {}  # Extra context data

    def __init__(self):
        """
        Initialize mixin.
        """
        if self.title_page:
            self.extra_context["title"] = self.title_page

        if self.cat_selected is not None:
            self.extra_context["cat_selected"] = self.cat_selected

    def get_mixin_context(self, context, **kwargs):
        """
        Method to update context with mixin data.
        """
        context["cat_selected"] = None
        context.update(kwargs)
        return context
