import logging

from django.urls import reverse
from wagtail.contrib.forms.models import FormSubmission
from wagtail.models import Page

from .base import UnveilURLFinder

logger = logging.getLogger(__name__)


class FormsAdminURLFinder(UnveilURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail Forms and Form Submissions.
    Provides comprehensive URL generation with permission checking and error handling.
    """
    
    def _get_forms_url_pattern_name(self, action):
        """
        Generate the correct URL pattern name for forms actions
        
        Args:
            action: The action (index, list_submissions, delete_submissions)
            
        Returns:
            String URL pattern name (e.g., 'wagtailforms:index')
        """
        return f"wagtailforms:{action}"
    
    def get_forms_index_url(self):
        """
        Get the main forms index URL
        
        Returns:
            String URL or None if not available
        """
        cache_key = "forms_index"
        url_pattern = self._get_forms_url_pattern_name('index')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern
        )

    def get_form_submissions_list_url(self, page_id):
        """
        Get the submissions list URL for a specific form page
        
        Args:
            page_id: The ID of the form page
            
        Returns:
            String URL or None if not available
        """
        if not page_id:
            return None
        
        cache_key = f"list_submissions_{page_id}"
        url_pattern = self._get_forms_url_pattern_name('list_submissions')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[page_id]
        )

    def get_form_submissions_delete_url(self, page_id):
        """
        Get the submissions delete URL for a specific form page
        
        Args:
            page_id: The ID of the form page
            
        Returns:
            String URL or None if not available
        """
        if not page_id:
            return None
        
        cache_key = f"delete_submissions_{page_id}"
        url_pattern = self._get_forms_url_pattern_name('delete_submissions')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[page_id]
        )
    
    def get_all_form_page_urls(self, page_id):
        """
        Get all available admin URLs for a form page
        
        Args:
            page_id: The ID of the form page
            
        Returns:
            Dict of URL types to URLs
        """
        if not page_id:
            return {}
            
        urls = {}
        url_methods = {
            'list_submissions': self.get_form_submissions_list_url,
            'delete_submissions': self.get_form_submissions_delete_url,
        }
        
        for url_type, method in url_methods.items():
            url = method(page_id)
            if url:
                urls[url_type] = url
                
        return urls


def get_form_pages_with_submissions():
    """
    Get all pages that have form submissions
    
    Returns:
        List of tuples: (page_id, page_title, page_class_name, submission_count)
    """
    form_pages = []
    
    # Get unique page IDs that have form submissions
    page_ids_with_submissions = FormSubmission.objects.values_list('page_id', flat=True).distinct()
    
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
            logger.warning(f"Page with ID {page_id} not found, but has form submissions")
        except Exception as e:
            logger.error(f"Error processing page {page_id}: {e}")
    
    return form_pages


def get_forms_urls(output, base_url, max_instances=10, user=None):
    """
    Generate URLs for Wagtail Forms using enhanced AdminURLFinder.
    
    Args:
        output: StringIO object for logging/debugging output
        base_url: Base URL for the site (e.g., "http://localhost:8000") - for admin URLs
        max_instances: Maximum number of form page URLs to generate
        user: Optional user for permission checking
        
    Returns:
        List of tuples: (model_name, url_type, url)
    """
    urls = []
    
    # Initialize the enhanced admin URL finder with user context
    url_finder = FormsAdminURLFinder(user)
    
    # Get the FormSubmission model name
    form_submission_model_name = f"{FormSubmission._meta.app_label}.{FormSubmission.__name__}"
    
    output.write(f"Processing Forms functionality\n")
    
    # Get forms index URL
    forms_index_url = url_finder.get_forms_index_url()
    if forms_index_url:
        urls.append((form_submission_model_name, "forms_index", f"{base_url}{forms_index_url}"))
    
    # Get form pages with submissions
    form_pages = get_form_pages_with_submissions()
    output.write(f"Found {len(form_pages)} form pages with submissions\n")
    
    # Limit the number of form pages processed
    limited_form_pages = form_pages[:max_instances]
    
    for page_id, page_title, page_class_name, submission_count in limited_form_pages:
        output.write(f"Processing form page: {page_title} (ID: {page_id}, {submission_count} submissions)\n")
        
        # Create a model identifier that includes the page info
        form_page_model_name = f"{form_submission_model_name}_Page_{page_id}"
        
        # Get all available admin URLs for this form page
        all_urls = url_finder.get_all_form_page_urls(page_id)
        
        # Add each URL type to our results
        for url_type, url in all_urls.items():
            urls.append((form_page_model_name, url_type, f"{base_url}{url}"))
        
        # Also add the frontend form URL if available
        try:
            page = Page.objects.get(id=page_id)
            frontend_url = page.url
            if frontend_url:
                urls.append((form_page_model_name, "frontend_form", f"{base_url.rstrip('/')}{frontend_url}"))
        except Exception as e:
            output.write(f"Error getting frontend URL for page {page_id}: {e}\n")
    
    output.write(f"Generated {len(urls)} forms URLs\n")
    return urls
