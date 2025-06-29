
from dataclasses import dataclass

from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.viewsets.base import ViewSet
from wagtail.models import Collection

from wagtail_unveil.models import UrlEntry
from wagtail_unveil.viewsets.base import UnveilReportView


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
            collection_model_name = f"wagtail.Collection ({collection.name})"
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


class UnveilCollectionReportIndexView(UnveilReportView):
    # Index view for the Collection Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Collection"
    header_icon = "folder-open-1"
    paginate_by = None
    
    def get_queryset(self):
        # Get the queryset for collection URLs
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 20 (collections are typically moderate in number)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
        
        # Collect collection URLs
        collection_urls = get_collection_urls(base_url, max_instances)
        for model_name, url_type, url in collection_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls
 

class UnveilCollectionReportViewSet(ViewSet):
    # ViewSet for Unveil Collection reports
    icon = "folder-open-1"
    menu_label = "Collection"
    menu_name = "unveil_collection_report"
    url_namespace = "unveil_collection_report"
    url_prefix = "unveil/collection-report"
    index_view_class = UnveilCollectionReportIndexView

    def as_json_view(self, request):
        # Require a token in the query string or header
        required_token = getattr(settings, 'WAGTAIL_UNVEIL_JSON_TOKEN', None)
        token = request.GET.get('token') or request.headers.get('X-API-TOKEN')
        if not required_token or token != required_token:
            return HttpResponseForbidden("Invalid or missing token.")
        # Return the collection report as JSON
        view = self.index_view_class()
        queryset = view.get_queryset()
        data = [
            {
                "id": entry.id,
                "model_name": entry.model_name,
                "url_type": entry.url_type,
                "url": entry.url,
            }
            for entry in queryset
        ]
        return JsonResponse({"results": data})

    def get_urlpatterns(self):
        # Return the URL patterns for this ViewSet
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
            path("json/", self.as_json_view, name="json"),
        ]


# Create an instance of the ViewSet to be registered
unveil_collection_viewset = UnveilCollectionReportViewSet()
