from collections import namedtuple
from io import StringIO

from django.conf import settings
from django.urls import path
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton

from ..helpers.settings import get_settings_urls


class UnveilSettingsReportIndexView(IndexView):
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Settings URL's"
    header_icon = "cog"
    paginate_by = None

    def get_queryset(self):
        output = StringIO()
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        user = self.request.user if self.request else None
        settings_urls = get_settings_urls(output, base_url, max_instances, user)
        for model_name, url_type, url in settings_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
        return all_urls

    def get_header_buttons(self):
        return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={"data-action": "check-urls"},
            )
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        return context


class UnveilSettingsReportViewSet(ViewSet):
    model = None
    icon = "cog"
    menu_label = "Settings URLs"
    menu_name = "unveil_settings_report"
    url_namespace = "unveil_settings_report"
    url_prefix = "unveil/settings-report"
    export_filename = "settings_urls"
    list_export = ["id", "model_name", "url_type", "url"]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }

    @property
    def index_view_class(self):
        return UnveilSettingsReportIndexView

    def get_urlpatterns(self):
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


unveil_settings_viewset = UnveilSettingsReportViewSet("unveil_settings_report")
