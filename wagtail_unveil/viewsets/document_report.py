from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.viewsets.base import ViewSet
from wagtail.documents import get_document_model

from wagtail_unveil.models import UrlEntry
from wagtail_unveil.viewsets.base import UnveilReportView


def get_document_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, full_url) for documents
    urls = []
    # Get the index URL for documents
    try:
        index_url = reverse('wagtaildocs:index')
        urls.append(('wagtail.Document', 'index', f"{base_url}{index_url}"))
    except NoReverseMatch:
        pass
    # Get the add URL for documents
    try:
        add_url = reverse('wagtaildocs:add')
        urls.append(('wagtail.Document', 'add', f"{base_url}{add_url}"))
    except NoReverseMatch:
        pass
    Document = get_document_model()
    try:
        documents = Document.objects.all()[:max_instances]
        for document in documents:
            document_model_name = f"wagtail.Document ({document.title})"
            # Get the edit URL for a document
            try:
                edit_url = reverse('wagtaildocs:edit', args=[document.id])
                urls.append((document_model_name, 'edit', f"{base_url}{edit_url}"))
            except NoReverseMatch:
                pass
            # Get the delete URL for a document
            try:
                delete_url = reverse('wagtaildocs:delete', args=[document.id])
                urls.append((document_model_name, 'delete', f"{base_url}{delete_url}"))
            except NoReverseMatch:
                pass
    except Document.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilDocumentReportIndexView(UnveilReportView):
    # Index view for the Document Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Document "
    header_icon = "doc-full-inverse"
    paginate_by = None
    
    def get_queryset(self):
        # Get the queryset for document URLs
        all_urls = []
        counter = 1
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
        document_urls = get_document_urls(base_url, max_instances)
        for model_name, url_type, url in document_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
        return all_urls


class UnveilDocumentReportViewSet(ViewSet):
    # ViewSet for Unveil Document reports
    icon = "doc-full-inverse"
    menu_label = "Document"
    menu_name = "unveil_document_report"
    url_namespace = "unveil_document_report"
    url_prefix = "unveil/document-report"
    index_view_class = UnveilDocumentReportIndexView
    
    def get_urlpatterns(self):
        # Return the URL patterns for this ViewSet
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]

# Create an instance of the ViewSet to be registered
unveil_document_viewset = UnveilDocumentReportViewSet("unveil_document_report")
