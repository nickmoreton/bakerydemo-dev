from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.models import Collection



def get_collection_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, full_url) for collections
    urls = []
    # Get the index URL for collections
    try:
        index_url = reverse('wagtailadmin_collections:index')
        urls.append(('wagtail.Collection', 'index', f"{base_url}{index_url}"))
    except NoReverseMatch:
        pass
    # Get the add URL for collections
    try:
        add_url = reverse('wagtailadmin_collections:add')
        urls.append(('wagtail.Collection', 'add', f"{base_url}{add_url}"))
    except NoReverseMatch:
        pass
    try:
        collections = Collection.objects.exclude(depth=1)[:max_instances]
        for collection in collections:
            collection_model_name = f"wagtail.Collection_{collection.id}_{collection.name}"
            # Get the edit URL for a collection
            try:
                edit_url = reverse('wagtailadmin_collections:edit', args=[collection.id])
                urls.append((collection_model_name, 'edit', f"{base_url}{edit_url}"))
            except NoReverseMatch:
                pass
            # Get the delete URL for a collection
            try:
                delete_url = reverse('wagtailadmin_collections:delete', args=[collection.id])
                urls.append((collection_model_name, 'delete', f"{base_url}{delete_url}"))
            except NoReverseMatch:
                pass
    except Collection.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilCollectionReportIndexView(IndexView):
    # Index view for the Collection Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Collection"
    header_icon = "folder-open-1"
    paginate_by = None
    
    def get_queryset(self):
        # Get the queryset for collection URLs
        
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
        
        # Collect collection URLs
        collection_urls = get_collection_urls(base_url, max_instances)
        for model_name, url_type, url in collection_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls
        
    def get_header_buttons(self):
        # Get header buttons
        return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]


class UnveilCollectionReportViewSet(ViewSet):
    # ViewSet for Unveil Collection reports
    icon = "folder-open-1"
    menu_label = "Collection"
    menu_name = "unveil_collection_report"
    url_namespace = "unveil_collection_report"
    url_prefix = "unveil/collection-report"
    index_view_class = UnveilCollectionReportIndexView
    
    def get_urlpatterns(self):
        # Return the URL patterns for this ViewSet
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


# Create an instance of the ViewSet to be registered
unveil_collection_viewset = UnveilCollectionReportViewSet()
