
from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.viewsets.base import ViewSet
from wagtail.models import Page, get_page_models

from wagtail_unveil.models import UrlEntry
from wagtail_unveil.viewsets.base import UnveilReportView


def get_page_urls(base_url, max_instances):
    """Return a list of tuples (model_name, url_type, full_url) for pages."""
    urls = []
    page_models = get_page_models()
    try:
        root_page = Page.objects.filter(depth=1).first()
    except Page.DoesNotExist:
        root_page = None
    for model in page_models:
        if model._meta.label_lower == 'wagtailcore.page':
            continue
        model_name = f"{model._meta.app_label}.{model.__name__}"
        # Add URL (if we have a root page)
        if root_page:
            try:
                add_url = reverse('wagtailadmin_pages:add', args=[model._meta.app_label, model._meta.model_name, root_page.pk])
                urls.append((model_name, 'add', f"{base_url}{add_url}"))
            except NoReverseMatch:
                pass
        try:
            if hasattr(model.objects, 'live'):
                instances = model.objects.live()[:max_instances] if max_instances else model.objects.live()
            else:
                instances = model.objects.all()[:max_instances] if max_instances else model.objects.all()
            for instance in instances:
                page_model_name = f"{model._meta.app_label}.{model.__name__} ({instance.title})"
                # Admin URLs
                for url_type, url_name in [
                    ('edit', 'wagtailadmin_pages:edit'),
                    ('delete', 'wagtailadmin_pages:delete'),
                    ('copy', 'wagtailadmin_pages:copy'),
                    ('move', 'wagtailadmin_pages:move'),
                    ('history', 'wagtailadmin_pages:history'),
                    ('workflow_history', 'wagtailadmin_pages:workflow_history'),
                ]:
                    try:
                        admin_url = reverse(url_name, args=[instance.id])
                        urls.append((page_model_name, url_type, f"{base_url}{admin_url}"))
                    except NoReverseMatch:
                        pass
                # Index URL
                try:
                    index_url = reverse('wagtailadmin_explore', args=[instance.id])
                    urls.append((page_model_name, 'index', f"{base_url}{index_url}"))
                except NoReverseMatch:
                    pass
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


class UnveilPageReportIndexView(UnveilReportView):
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
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
        page_urls = get_page_urls(base_url, max_instances)
        for model_name, url_type, url in page_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


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
