from wagtail.admin.views.reports import ReportView
from collections import namedtuple
from io import StringIO
from wagtail.admin.widgets.button import HeaderButton
from django.conf import settings

from .helpers.page_helpers import get_page_urls
# from .helpers.snippet_helpers import get_snippet_urls, get_modelviewset_urls
# from .helpers.modeladmin_helpers import get_modeladmin_urls
# from .helpers.settings_helpers import get_settings_admin_urls
# from .helpers.media_helpers import get_image_admin_urls, get_document_admin_urls


class UnveilReportView(ReportView):
    index_url_name = "unveil_report"
    index_results_url_name = "unveil_report_results"
    header_icon = "tasks"
    template_name = "wagtail_unveil/unveil_report.html"
    results_template_name = "wagtail_unveil/unveil_report_results.html"
    page_title = "Unveil URL's"
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
        # Get max_instances from settings with a default of 1
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect page URLs
        page_urls = get_page_urls(output, base_url, max_instances)
        for model_name, url_type, url in page_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
        
        # # Get snippet models and collect snippet URLs
        # snippet_urls = get_snippet_urls(output, base_url, max_instances)
        # for model_name, url_type, url in snippet_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
        
        # # Create an empty dictionary for URL paths since we no longer get it from get_modelviewset_models()
        # modelviewset_urls = get_modelviewset_urls(output, base_url, max_instances)
        # for model_name, url_type, url in modelviewset_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
        
        # # Get modeladmin models and collect modeladmin URLs
        # modeladmin_urls = get_modeladmin_urls(output, base_url, max_instances)
        # for model_name, url_type, url in modeladmin_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
        
        # # Collect settings URLs
        # settings_urls = get_settings_admin_urls(output, base_url)
        # for model_name, url_type, url in settings_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
        
        # # Get image URLs
        # image_urls = get_image_admin_urls(output, base_url, max_instances)
        # for model_name, url_type, url in image_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
            
        # # Get document URLs
        # document_urls = get_document_admin_urls(output, base_url, max_instances)
        # for model_name, url_type, url in document_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
            
        return all_urls