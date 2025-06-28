from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.snippets.models import get_snippet_models


def get_snippet_url_pattern_name(model, action):
    """Generate the correct URL pattern name for a snippet model and action."""
    app_label = model._meta.app_label
    model_name = model._meta.model_name
    return f"wagtailsnippets_{app_label}_{model_name}:{action}"

def get_snippet_add_url(model):
    """Get the add URL for creating a new snippet of the given model type."""
    try:
        url_pattern = get_snippet_url_pattern_name(model, 'add')
        return reverse(url_pattern)
    except NoReverseMatch:
        return None

def get_snippet_list_url(model):
    """Get the list URL for the given snippet model."""
    try:
        url_pattern = get_snippet_url_pattern_name(model, 'list')
        return reverse(url_pattern)
    except NoReverseMatch:
        return None

def get_snippet_edit_url(instance):
    """Get the edit URL for a snippet instance."""
    try:
        model = type(instance)
        url_pattern = get_snippet_url_pattern_name(model, 'edit')
        return reverse(url_pattern, args=[instance.pk])
    except NoReverseMatch:
        return None

def get_snippet_delete_url(instance):
    """Get the delete URL for a snippet instance."""
    try:
        model = type(instance)
        url_pattern = get_snippet_url_pattern_name(model, 'delete')
        return reverse(url_pattern, args=[instance.pk])
    except NoReverseMatch:
        return None

def get_snippet_copy_url(instance):
    """Get the copy URL for a snippet instance."""
    try:
        model = type(instance)
        url_pattern = get_snippet_url_pattern_name(model, 'copy')
        return reverse(url_pattern, args=[instance.pk])
    except NoReverseMatch:
        return None

def get_snippet_history_url(instance):
    """Get the history URL for a snippet instance."""
    try:
        model = type(instance)
        url_pattern = get_snippet_url_pattern_name(model, 'history')
        return reverse(url_pattern, args=[instance.pk])
    except NoReverseMatch:
        return None

def get_snippet_usage_url(instance):
    """Get the usage URL for a snippet instance."""
    try:
        model = type(instance)
        url_pattern = get_snippet_url_pattern_name(model, 'usage')
        return reverse(url_pattern, args=[instance.pk])
    except NoReverseMatch:
        return None

def get_snippet_urls(base_url, max_instances, user=None):
    """Return a list of tuples (model_name, url_type, full_url) for snippets."""
    urls = []
    
    # Get all snippet models
    snippet_models = get_snippet_models()
    
    for model in snippet_models:
        model_name = f"{model._meta.app_label}.{model.__name__}"
        
        # Add URL
        add_url = get_snippet_add_url(model)
        if add_url:
            urls.append((model_name, 'add', f"{base_url}{add_url}"))
        
        # List URL
        list_url = get_snippet_list_url(model)
        if list_url:
            urls.append((model_name, 'list', f"{base_url}{list_url}"))
        
        try:
            # Get instances
            instances = model.objects.all()[:max_instances] if max_instances else model.objects.all()
            
            for instance in instances:
                snippet_model_name = f"{model._meta.app_label}.{model.__name__}_{instance.id}_{getattr(instance, 'title', getattr(instance, 'name', str(instance)))}"
                
                # Admin URLs
                edit_url = get_snippet_edit_url(instance)
                if edit_url:
                    urls.append((snippet_model_name, 'edit', f"{base_url}{edit_url}"))
                
                delete_url = get_snippet_delete_url(instance)
                if delete_url:
                    urls.append((snippet_model_name, 'delete', f"{base_url}{delete_url}"))
                
                copy_url = get_snippet_copy_url(instance)
                if copy_url:
                    urls.append((snippet_model_name, 'copy', f"{base_url}{copy_url}"))
                
                history_url = get_snippet_history_url(instance)
                if history_url:
                    urls.append((snippet_model_name, 'history', f"{base_url}{history_url}"))
                
                usage_url = get_snippet_usage_url(instance)
                if usage_url:
                    urls.append((snippet_model_name, 'usage', f"{base_url}{usage_url}"))
                    
        except (model.DoesNotExist, AttributeError, ValueError, TypeError):
            pass
    
    return urls


class UnveilSnippetReportIndexView(IndexView):
    """
    Custom index view for the Snippet Report ViewSet.
    """
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Snippet"
    header_icon = "sliders"
    paginate_by = None

    def get_queryset(self):
        """Generate the queryset for snippet URLs."""
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        user = self.request.user if self.request else None
        
        snippet_urls = get_snippet_urls(base_url, max_instances, user)
        for model_name, url_type, url in snippet_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls

    def get_header_buttons(self):
        """Get buttons to display in the header."""
        return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={"data-action": "check-urls"},
            )
        ]


class UnveilSnippetReportViewSet(ViewSet):
    """
    ViewSet for Unveil Snippet reports using Wagtail's ViewSet pattern.
    """
    icon = "sliders"
    menu_label = "Snippet"
    menu_name = "unveil_snippet_report"
    url_namespace = "unveil_snippet_report"
    url_prefix = "unveil/snippet-report"
    index_view_class = UnveilSnippetReportIndexView
    
    def get_urlpatterns(self):
        """Return the URL patterns for this ViewSet."""
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


# Create an instance of the ViewSet to be registered
unveil_snippet_viewset = UnveilSnippetReportViewSet("unveil_snippet_report")
