from django.conf import settings
from django.urls import NoReverseMatch, reverse
from wagtail.models import Locale

from wagtail_unveil.models import UrlEntry
from wagtail_unveil.viewsets.base import UnveilReportView, UnveilReportViewSet


def get_locale_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, url) for locales
    urls = []
    # Get the index URL for locales
    try:
        index_url = reverse('wagtaillocales:index')
        urls.append(('wagtail.Locale', 'index', f"{base_url}{index_url}"))
    except NoReverseMatch:
        pass
    # add_url = get_locale_add_url()  # This path doesn't exist for this model
    # if add_url:
    #     urls.append(('wagtail.Locale', 'add', f"{base_url}{add_url}"))
    try:
        locales = Locale.objects.all()[:max_instances]
        for locale in locales:
            locale_model_name = f"wagtail.Locale ({getattr(locale, 'language_code', getattr(locale, 'code', ''))})"
            # Get the edit URL for a locale
            try:
                edit_url = reverse('wagtaillocales:edit', args=[locale.id])
                urls.append((locale_model_name, 'edit', f"{base_url}{edit_url}"))
            except NoReverseMatch:
                pass
            # Get the delete URL for a locale
            try:
                delete_url = reverse('wagtaillocales:delete', args=[locale.id])
                urls.append((locale_model_name, 'delete', f"{base_url}{delete_url}"))
            except NoReverseMatch:
                pass
    except Locale.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilLocaleReportIndexView(UnveilReportView):
    # Index view for the Locale Report
    api_slug = "locale"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Locale "
    header_icon = "globe"
    paginate_by = None

    def get_queryset(self):
        # Get the queryset for locale URLs
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
        locale_urls = get_locale_urls(base_url, max_instances)
        for model_name, url_type, url in locale_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
        return all_urls


class UnveilLocaleReportViewSet(UnveilReportViewSet):
    # ViewSet for Unveil Locale reports
    icon = "globe"
    menu_label = "Locale"
    menu_name = "unveil_locale_report"
    url_namespace = "unveil_locale_report"
    url_prefix = "unveil/locale-report"
    index_view_class = UnveilLocaleReportIndexView


unveil_locale_viewset = UnveilLocaleReportViewSet("unveil_locale_report")
