from collections import namedtuple
from io import StringIO

from django.conf import settings
from django.urls import path
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton

from ..helpers.redirect import get_redirects_urls


class UnveilRedirectReportIndexView(IndexView):
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Redirect "
    header_icon = "redirect"
    paginate_by = None

    def get_queryset(self):
        output = StringIO()
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        user = self.request.user if self.request else None
        redirect_urls = get_redirects_urls(output, base_url, max_instances, user)
        for model_name, url_type, url in redirect_urls:
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


class UnveilRedirectReportViewSet(ViewSet):
    model = None
    icon = "redirect"
    menu_label = "Redirect"
    menu_name = "unveil_redirect_report"
    url_namespace = "unveil_redirect_report"
    url_prefix = "unveil/redirect-report"
    export_filename = "redirect_urls"
    list_export = ["id", "model_name", "url_type", "url"]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }

    @property
    def index_view_class(self):
        return UnveilRedirectReportIndexView

    def get_urlpatterns(self):
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


unveil_redirect_viewset = UnveilRedirectReportViewSet("unveil_redirect_report")
