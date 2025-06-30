from django.conf import settings

from wagtail_unveil.models import UrlEntry
from wagtail_unveil.viewsets.base import UnveilReportView, UnveilReportViewSet


def get_admin_urls(base_url, max_instances):
    """
    Get admin urls that we don't need a model for.
    Returns a list of tuples: (model_name, url_type, url)
    - Admin index
    - Admin login
    - Admin password reset
    - Admin password change
    - Admin user profile
    """
    urls = [
        ("wagtail.Admin", "index", f"{base_url}/admin/"),
        ("wagtail.Admin", "login", f"{base_url}/admin/login/"),
        ("wagtail.Admin", "password_reset", f"{base_url}/admin/password_reset/"),
        ("wagtail.Admin", "user_profile", f"{base_url}/admin/account/"),
    ]

    # Add custom admin URLs from settings
    custom_admin_urls = getattr(settings, 'WAGTAIL_UNVEIL_ADMIN_URLS', [])
    for url in custom_admin_urls:
        try:
            url_name = url.get('name', '')
            url_type = url.get('type', 'custom')
            full_url = f"{base_url}admin/{url_name}/"
            urls.append((f"wagtail.Admin ({url_name})", url_type, full_url))
        except KeyError:
            continue
    return urls


class UnveilAdminReportIndexView(UnveilReportView):
    api_slug = "admin"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Admin"
    header_icon = "cog"
    paginate_by = None

    def get_queryset(self):
        all_urls = []
        counter = 1
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
        admin_urls = get_admin_urls(base_url, max_instances)
        for model_name, url_type, url in admin_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
        return all_urls


class UnveilAdminReportViewSet(UnveilReportViewSet):
    icon = "cog"
    menu_label = "Admin"
    menu_name = "unveil_admin_report"
    url_namespace = "unveil_admin_report"
    url_prefix = "unveil/admin-report"
    index_view_class = UnveilAdminReportIndexView


# Create an instance of the ViewSet to be registered
unveil_admin_viewset = UnveilAdminReportViewSet("unveil_admin_report")

