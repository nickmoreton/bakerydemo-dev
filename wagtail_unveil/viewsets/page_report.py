from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.models import Page, get_page_models


def get_page_add_url(app_label, model_name, parent_id):
    """Get the add URL for creating a new page of the given model type."""
    try:
        return reverse('wagtailadmin_pages:add', args=[app_label, model_name, parent_id])
    except NoReverseMatch:
        return None

def get_page_edit_url(page_id):
    """Get the edit URL for a page."""
    try:
        return reverse('wagtailadmin_pages:edit', args=[page_id])
    except NoReverseMatch:
        return None

def get_page_delete_url(page_id):
    """Get the delete URL for a page."""
    try:
        return reverse('wagtailadmin_pages:delete', args=[page_id])
    except NoReverseMatch:
        return None

def get_page_copy_url(page_id):
    """Get the copy URL for a page."""
    try:
        return reverse('wagtailadmin_pages:copy', args=[page_id])
    except NoReverseMatch:
        return None

def get_page_move_url(page_id):
    """Get the move URL for a page."""
    try:
        return reverse('wagtailadmin_pages:move', args=[page_id])
    except NoReverseMatch:
        return None

def get_page_history_url(page_id):
    """Get the history URL for a page."""
    try:
        return reverse('wagtailadmin_pages:history', args=[page_id])
    except NoReverseMatch:
        return None

def get_page_workflow_history_url(page_id):
    """Get the workflow history URL for a page."""
    try:
        return reverse('wagtailadmin_pages:workflow_history', args=[page_id])
    except NoReverseMatch:
        return None

def get_page_index_url(page_id):
    """Get the index/list URL for a page (shows children/subpages)."""
    try:
        return reverse('wagtailadmin_explore', args=[page_id])
    except NoReverseMatch:
        return None

def get_page_urls(base_url, max_instances):
    """Return a list of tuples (model_name, url_type, full_url) for pages."""
    urls = []
    
    # Get all Page models
    page_models = get_page_models()
    
    # Get root page for add URLs
    try:
        root_page = Page.objects.filter(depth=1).first()
    except Page.DoesNotExist:
        root_page = None
    
    for model in page_models:
        # Skip the base Page model
        if model._meta.label_lower == 'wagtailcore.page':
            continue
            
        model_name = f"{model._meta.app_label}.{model.__name__}"
        
        # Add URL (if we have a root page)
        if root_page:
            add_url = get_page_add_url(model._meta.app_label, model._meta.model_name, root_page.pk)
            if add_url:
                urls.append((model_name, 'add', f"{base_url}{add_url}"))
        
        try:
            # Get instances, prefer live pages if available
            if hasattr(model.objects, 'live'):
                instances = model.objects.live()[:max_instances] if max_instances else model.objects.live()
            else:
                instances = model.objects.all()[:max_instances] if max_instances else model.objects.all()
            
            for instance in instances:
                page_model_name = f"{model._meta.app_label}.{model.__name__}_{instance.id}_{instance.title}"
                
                # Admin URLs
                edit_url = get_page_edit_url(instance.id)
                if edit_url:
                    urls.append((page_model_name, 'edit', f"{base_url}{edit_url}"))
                
                delete_url = get_page_delete_url(instance.id)
                if delete_url:
                    urls.append((page_model_name, 'delete', f"{base_url}{delete_url}"))
                
                copy_url = get_page_copy_url(instance.id)
                if copy_url:
                    urls.append((page_model_name, 'copy', f"{base_url}{copy_url}"))
                
                move_url = get_page_move_url(instance.id)
                if move_url:
                    urls.append((page_model_name, 'move', f"{base_url}{move_url}"))
                
                history_url = get_page_history_url(instance.id)
                if history_url:
                    urls.append((page_model_name, 'history', f"{base_url}{history_url}"))
                
                workflow_history_url = get_page_workflow_history_url(instance.id)
                if workflow_history_url:
                    urls.append((page_model_name, 'workflow_history', f"{base_url}{workflow_history_url}"))
                
                index_url = get_page_index_url(instance.id)
                if index_url:
                    urls.append((page_model_name, 'index', f"{base_url}{index_url}"))
                
                # Frontend view URL
                if hasattr(instance, 'url') and instance.url:
                    view_url = instance.url
                    if not view_url.startswith('http'):
                        if view_url.startswith('/'):
                            view_url = f"{base_url}{view_url}"
                        else:
                            view_url = f"{base_url}/{view_url}"
                    urls.append((page_model_name, 'view', view_url))
                    
        except (model.DoesNotExist, AttributeError, ValueError, TypeError):
            pass
    
    return urls


class UnveilPageReportIndexView(IndexView):
    """
    Custom index view for the Page Report ViewSet.
    """
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Page"
    header_icon = "pilcrow"
    paginate_by = None

    def get_queryset(self):
        """Generate the queryset for page URLs."""
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        page_urls = get_page_urls(base_url, max_instances)
        for model_name, url_type, url in page_urls:
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


class UnveilPageReportViewSet(ViewSet):
    """
    ViewSet for Unveil Page reports using Wagtail's ViewSet pattern.
    """
    icon = "pilcrow"
    menu_label = "Page"
    menu_name = "unveil_page_report"
    url_namespace = "unveil_page_report"
    url_prefix = "unveil/page-report"
    index_view_class = UnveilPageReportIndexView
    
    def get_urlpatterns(self):
        """Return the URL patterns for this ViewSet."""
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


# Create an instance of the ViewSet to be registered
unveil_page_viewset = UnveilPageReportViewSet("unveil_page_report")
