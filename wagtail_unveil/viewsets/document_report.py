from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.documents import get_document_model


def get_document_index_url():
    try:
        return reverse('wagtaildocs:index')
    except NoReverseMatch:
        return None

def get_document_add_url():
    try:
        return reverse('wagtaildocs:add')
    except NoReverseMatch:
        return None

def get_document_edit_url(document_id):
    try:
        return reverse('wagtaildocs:edit', args=[document_id])
    except NoReverseMatch:
        return None

def get_document_delete_url(document_id):
    try:
        return reverse('wagtaildocs:delete', args=[document_id])
    except NoReverseMatch:
        return None

def get_document_urls(base_url, max_instances, user=None):
    """Return a list of tuples (model_name, url_type, full_url) for documents."""
    urls = []
    index_url = get_document_index_url()
    if index_url:
        urls.append(('wagtail.Document', 'index', f"{base_url}{index_url}"))
    add_url = get_document_add_url()
    if add_url:
        urls.append(('wagtail.Document', 'add', f"{base_url}{add_url}"))
    Document = get_document_model()
    try:
        documents = Document.objects.all()[:max_instances]
        for document in documents:
            document_model_name = f"wagtail.Document_{document.id}_{document.title}"
            edit_url = get_document_edit_url(document.id)
            if edit_url:
                urls.append((document_model_name, 'edit', f"{base_url}{edit_url}"))
            delete_url = get_document_delete_url(document.id)
            if delete_url:
                urls.append((document_model_name, 'delete', f"{base_url}{delete_url}"))
    except Document.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilDocumentReportIndexView(IndexView):
    """
    Custom index view for the Document Report ViewSet.
    """
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Document "
    header_icon = "doc-full-inverse" 
    paginate_by = None
    
    def get_queryset(self):
        """Generate the queryset for document URLs."""
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"
        user = self.request.user if self.request else None
        document_urls = get_document_urls(base_url, max_instances, user)
        for model_name, url_type, url in document_urls:
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


class UnveilDocumentReportViewSet(ViewSet):
    """
    ViewSet for Unveil Document reports using Wagtail's ViewSet pattern.
    """
    icon = "doc-full-inverse"
    menu_label = "Document"
    menu_name = "unveil_document_report"
    url_namespace = "unveil_document_report"
    url_prefix = "unveil/document-report"
    index_view_class = UnveilDocumentReportIndexView
    
    def get_urlpatterns(self):
        """Return the URL patterns for this ViewSet."""
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]

# Create an instance of the ViewSet to be registered
unveil_document_viewset = UnveilDocumentReportViewSet("unveil_document_report")
