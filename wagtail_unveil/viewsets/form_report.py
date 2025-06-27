from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, reverse, path
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.contrib.forms.models import FormSubmission
from wagtail.models import Page


def get_forms_index_url():
    """Get the main forms index URL."""
    try:
        return reverse('wagtailforms:index')
    except NoReverseMatch:
        return None


def get_form_submissions_list_url(page_id):
    """Get the submissions list URL for a specific form page."""
    if not page_id:
        return None
    try:
        return reverse('wagtailforms:list_submissions', args=[page_id])
    except NoReverseMatch:
        return None


def get_form_submissions_delete_url(page_id):
    """Get the submissions delete URL for a specific form page."""
    if not page_id:
        return None
    try:
        return reverse('wagtailforms:delete_submissions', args=[page_id])
    except NoReverseMatch:
        return None


def get_form_pages_with_submissions():
    """
    Get all pages that have form submissions.
    
    Returns:
        List of tuples: (page_id, page_title, page_class_name, submission_count)
    """
    form_pages = []
    
    # Get unique page IDs that have form submissions
    try:
        page_ids_with_submissions = FormSubmission.objects.values_list('page_id', flat=True).distinct()
    except Exception:
        return form_pages
    
    for page_id in page_ids_with_submissions:
        try:
            page = Page.objects.get(id=page_id)
            specific_page = page.specific
            submission_count = FormSubmission.objects.filter(page_id=page_id).count()
            
            form_pages.append((
                page_id,
                page.title,
                specific_page.__class__.__name__,
                submission_count
            ))
        except Page.DoesNotExist:
            continue
        except Exception:
            continue
    
    return form_pages


def get_forms_urls(base_url, max_instances=10):
    """
    Generate URLs for Wagtail Forms.
    
    Args:
        base_url: Base URL for the site (e.g., "http://localhost:8000")
        max_instances: Maximum number of form page URLs to generate
        
    Returns:
        List of tuples: (model_name, url_type, url)
    """
    urls = []
    
    # Get the FormSubmission model name
    form_submission_model_name = f"{FormSubmission._meta.app_label}.{FormSubmission.__name__}"
    
    # Get forms index URL
    forms_index_url = get_forms_index_url()
    if forms_index_url:
        urls.append((form_submission_model_name, "forms_index", f"{base_url}{forms_index_url}"))
    
    # Get form pages with submissions
    form_pages = get_form_pages_with_submissions()
    
    # Limit the number of form pages processed
    if max_instances:
        limited_form_pages = form_pages[:max_instances]
    else:
        limited_form_pages = form_pages
    
    for page_id, page_title, page_class_name, submission_count in limited_form_pages:
        # Create a model identifier that includes the page info
        form_page_model_name = f"{form_submission_model_name}_Page_{page_id}"
        
        # Get submissions list URL
        list_url = get_form_submissions_list_url(page_id)
        if list_url:
            urls.append((form_page_model_name, "list_submissions", f"{base_url}{list_url}"))
        
        # Get submissions delete URL
        delete_url = get_form_submissions_delete_url(page_id)
        if delete_url:
            urls.append((form_page_model_name, "delete_submissions", f"{base_url}{delete_url}"))
        
        # Also add the frontend form URL if available
        try:
            page = Page.objects.get(id=page_id)
            frontend_url = page.url
            if frontend_url:
                urls.append((form_page_model_name, "frontend_form", f"{base_url.rstrip('/')}{frontend_url}"))
        except Exception:
            pass
    
    return urls


class UnveilFormReportIndexView(IndexView):
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Form "
    header_icon = "form"
    paginate_by = None

    def get_queryset(self):
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        form_urls = get_forms_urls(base_url, max_instances)
        for model_name, url_type, url in form_urls:
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


class UnveilFormReportViewSet(ViewSet):
    model = None
    icon = "form"
    menu_label = "Form"
    menu_name = "unveil_form_report"
    url_namespace = "unveil_form_report"
    url_prefix = "unveil/form-report"
    index_view_class = UnveilFormReportIndexView

    def get_urlpatterns(self):
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


unveil_form_viewset = UnveilFormReportViewSet("unveil_form_report")
