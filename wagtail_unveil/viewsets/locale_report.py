from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.models import Locale


def get_locale_index_url():
    # Get the index URL for locales
    try:
        return reverse('wagtaillocales:index')
    except NoReverseMatch:
        return None


# wagtaillocales:add This path doesn't exist for this model

def get_locale_edit_url(locale_id):
    # Get the edit URL for a locale
    try:
        return reverse('wagtaillocales:edit', args=[locale_id])
    except NoReverseMatch:
        return None


def get_locale_delete_url(locale_id):
    # Get the delete URL for a locale
    try:
        return reverse('wagtaillocales:delete', args=[locale_id])
    except NoReverseMatch:
        return None


def get_locale_urls(base_url, max_instances, user=None):
    # Return a list of tuples (model_name, url_type, url) for locales
    urls = []
    index_url = get_locale_index_url()
    if index_url:
        urls.append(('wagtail.Locale', 'index', f"{base_url}{index_url}"))
    # add_url = get_locale_add_url()
    # if add_url:
    #     urls.append(('wagtail.Locale', 'add', f"{base_url}{add_url}"))
    try:
        locales = Locale.objects.all()[:max_instances]
        for locale in locales:
            locale_model_name = f"wagtail.Locale_{locale.id}_{getattr(locale, 'language_code', getattr(locale, 'code', ''))}"
            edit_url = get_locale_edit_url(locale.id)
            if edit_url:
                urls.append((locale_model_name, 'edit', f"{base_url}{edit_url}"))
            delete_url = get_locale_delete_url(locale.id)
            if delete_url:
                urls.append((locale_model_name, 'delete', f"{base_url}{delete_url}"))
    except Locale.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilLocaleReportIndexView(IndexView):
    # Index view for the Locale Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Locale "
    header_icon = "globe"
    paginate_by = None

    def get_queryset(self):
        # Get the queryset for locale URLs
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        user = self.request.user if self.request else None
        locale_urls = get_locale_urls(base_url, max_instances, user)
        for model_name, url_type, url in locale_urls:
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

    def get_context_data(self, **kwargs):
        # Get context data
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        return context


class UnveilLocaleReportViewSet(ViewSet):
    # ViewSet for Unveil Locale reports
    icon = "globe"
    menu_label = "Locale"
    menu_name = "unveil_locale_report"
    url_namespace = "unveil_locale_report"
    url_prefix = "unveil/locale-report"
    index_view_class = UnveilLocaleReportIndexView

    def get_urlpatterns(self):
        # Return the URL patterns for this ViewSet
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


unveil_locale_viewset = UnveilLocaleReportViewSet("unveil_locale_report")
