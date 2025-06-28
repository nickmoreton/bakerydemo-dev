from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.contrib.redirects.models import Redirect


def get_redirect_index_url():
    # Get the index URL for redirects
    try:
        return reverse('wagtailredirects:index')
    except NoReverseMatch:
        return None


def get_redirect_add_url():
    # Get the add URL for redirects
    try:
        return reverse('wagtailredirects:add')
    except NoReverseMatch:
        return None


def get_redirect_edit_url(redirect_id):
    # Get the edit URL for a redirect
    try:
        return reverse('wagtailredirects:edit', args=[redirect_id])
    except NoReverseMatch:
        return None


def get_redirect_delete_url(redirect_id):
    # Get the delete URL for a redirect
    try:
        return reverse('wagtailredirects:delete', args=[redirect_id])
    except NoReverseMatch:
        return None


def get_redirect_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, url) for redirects
    urls = []
    index_url = get_redirect_index_url()
    if index_url:
        urls.append(('wagtail.Redirect', 'index', f"{base_url}{index_url}"))
    add_url = get_redirect_add_url()
    if add_url:
        urls.append(('wagtail.Redirect', 'add', f"{base_url}{add_url}"))
    try:
        redirects = Redirect.objects.all()[:max_instances]
        for redirect in redirects:
            redirect_model_name = f"wagtail.Redirect_{redirect.id}_{getattr(redirect, 'old_path', '')}"
            edit_url = get_redirect_edit_url(redirect.id)
            if edit_url:
                urls.append((redirect_model_name, 'edit', f"{base_url}{edit_url}"))
            delete_url = get_redirect_delete_url(redirect.id)
            if delete_url:
                urls.append((redirect_model_name, 'delete', f"{base_url}{delete_url}"))
    except Redirect.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilRedirectReportIndexView(IndexView):
    # Index view for the Redirect Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Redirect"
    header_icon = "redirect"
    paginate_by = None

    def get_queryset(self):
        # Get the queryset for redirect URLs
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        redirect_urls = get_redirect_urls(base_url, max_instances)
        for model_name, url_type, url in redirect_urls:
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
            ),
        ]


class UnveilRedirectReportViewSet(ViewSet):
    # ViewSet for Unveil Redirect reports
    icon = "redirect"
    menu_label = "Redirect"
    menu_name = "unveil_redirect_report"
    url_namespace = "unveil_redirect_report"
    url_prefix = "unveil/redirect-report"
    index_view_class = UnveilRedirectReportIndexView

    def get_urlpatterns(self):
        # Return the URL patterns for this ViewSet
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


# Create an instance of the ViewSet to be registered
unveil_redirect_viewset = UnveilRedirectReportViewSet()
