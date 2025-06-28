from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.models import Site


def get_site_index_url():
    # Get the index URL for sites
    try:
        return reverse('wagtailsites:index')
    except NoReverseMatch:
        return None

def get_site_add_url():
    # Get the add URL for sites
    try:
        return reverse('wagtailsites:add')
    except NoReverseMatch:
        return None

def get_site_edit_url(site_id):
    # Get the edit URL for a site
    try:
        return reverse('wagtailsites:edit', args=[site_id])
    except NoReverseMatch:
        return None

def get_site_delete_url(site_id):
    # Get the delete URL for a site
    try:
        return reverse('wagtailsites:delete', args=[site_id])
    except NoReverseMatch:
        return None

def get_site_frontend_url(site):
    # Get the frontend URL for a site instance
    if not site:
        return None
    
    # Build the frontend URL from site hostname and port
    protocol = "https" if site.port == 443 else "http"
    if site.port in [80, 443]:
        return f"{protocol}://{site.hostname}/"
    else:
        return f"{protocol}://{site.hostname}:{site.port}/"

def get_site_urls(base_url, max_instances, user=None):
    # Return a list of tuples (model_name, url_type, full_url) for sites
    urls = []
    
    # Add index and add URLs
    index_url = get_site_index_url()
    if index_url:
        urls.append(('wagtail.Site', 'index', f"{base_url}{index_url}"))
    
    add_url = get_site_add_url()
    if add_url:
        urls.append(('wagtail.Site', 'add', f"{base_url}{add_url}"))
    
    try:
        sites = Site.objects.all()[:max_instances] if max_instances else Site.objects.all()
        for site in sites:
            site_model_name = f"wagtail.Site_{site.id}_{site.hostname}"
            
            # Admin URLs
            edit_url = get_site_edit_url(site.id)
            if edit_url:
                urls.append((site_model_name, 'edit', f"{base_url}{edit_url}"))
            
            delete_url = get_site_delete_url(site.id)
            if delete_url:
                urls.append((site_model_name, 'delete', f"{base_url}{delete_url}"))
            
            # Frontend URL (actual site URL)
            frontend_url = get_site_frontend_url(site)
            if frontend_url:
                urls.append((site_model_name, 'frontend', frontend_url))
                
    except Site.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    
    return urls


class UnveilSiteReportIndexView(IndexView):
    # Index view for the Site Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Site"
    header_icon = "home"
    paginate_by = None

    def get_queryset(self):
        # Get the queryset for site URLs
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        user = self.request.user if self.request else None
        
        site_urls = get_site_urls(base_url, max_instances, user)
        for model_name, url_type, url in site_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls

    def get_header_buttons(self):
        # Get header buttons
        return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={"data-action": "check-urls"},
            )
        ]


class UnveilSiteReportViewSet(ViewSet):
    # ViewSet for Unveil Site reports
    icon = "home"
    menu_label = "Site"
    menu_name = "unveil_site_report"
    url_namespace = "unveil_site_report"
    url_prefix = "unveil/site-report"
    index_view_class = UnveilSiteReportIndexView
    
    def get_urlpatterns(self):
        # Return the URL patterns for this ViewSet
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


# Create an instance of the ViewSet to be registered
unveil_site_viewset = UnveilSiteReportViewSet("unveil_site_report")
