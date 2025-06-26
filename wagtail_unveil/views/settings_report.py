from collections import namedtuple
from io import StringIO

from django.conf import settings
from wagtail.admin.views.reports import ReportView
from wagtail.admin.widgets.button import HeaderButton

from ..helpers.settings_helpers import get_settings_urls


class UnveilSettingsReportView(ReportView):
    index_url_name = "unveil_settings_report"
    index_results_url_name = "unveil_settings_report_results"
    header_icon = "cog"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Settings URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 10 (settings models are typically few)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 10)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect settings URLs
        settings_urls = get_settings_urls(output, base_url, max_instances, self.request.user)
        for model_name, url_type, url in settings_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls
