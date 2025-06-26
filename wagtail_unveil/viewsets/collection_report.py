from collections import namedtuple
from io import StringIO

from django.conf import settings
from django.urls import path
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton

from ..helpers.collection import get_collection_urls


class UnveilCollectionReportIndexView(IndexView):
    """
    Custom index view for the Collection Report ViewSet.
    """
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Collection"
    header_icon = "folder-open-1" 
    paginate_by = None
    
    def get_queryset(self):
        """Generate the queryset for collection URLs."""
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 20 (collections are typically moderate in number)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Get current user from request
        user = self.request.user if self.request else None
        
        # Collect collection URLs
        collection_urls = get_collection_urls(output, base_url, max_instances, user)
        for model_name, url_type, url in collection_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls
        
    def get_header_buttons(self):
        """Get buttons to display in the header."""
        return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_queryset()
        return context


class UnveilCollectionReportViewSet(ViewSet):
    """
    ViewSet for Unveil Collection reports using Wagtail's ViewSet pattern.
    
    This provides an alternative to the ReportView-based implementation,
    offering more flexibility and better integration with Wagtail's admin interface.
    """
    
    # Basic ViewSet configuration
    model = None  # We don't have a specific model as this is a report
    icon = "folder-open-1"
    menu_label = "Collection"
    menu_name = "unveil_collection_report"
    url_namespace = "unveil_collection_report"
    url_prefix = "unveil/collection-report"
    index_view_class = UnveilCollectionReportIndexView
    
    # Export configuration
    export_filename = "collection_urls"
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

    
    def get_urlpatterns(self):
        """Return the URL patterns for this ViewSet."""
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


# Create an instance of the ViewSet to be registered
unveil_collection_viewset = UnveilCollectionReportViewSet("unveil_collection_report")
