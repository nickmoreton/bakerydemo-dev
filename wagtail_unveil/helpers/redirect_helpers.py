import logging

from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch, reverse
from wagtail.admin.admin_url_finder import ModelAdminURLFinder
from wagtail.contrib.redirects.models import Redirect

logger = logging.getLogger(__name__)


class RedirectsAdminURLFinder(ModelAdminURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail Redirects.
    Provides comprehensive URL generation with permission checking and error handling.
    """
    
    def __init__(self, user=None):
        """
        Initialize with optional user for permission checking
        """
        super().__init__(user)
        self._url_cache = {}
    
    def _get_cached_url(self, cache_key, url_func, *args, **kwargs):
        """
        Get URL from cache or generate and cache it
        """
        if cache_key not in self._url_cache:
            try:
                self._url_cache[cache_key] = url_func(*args, **kwargs)
            except (NoReverseMatch, ImproperlyConfigured) as e:
                logger.warning(f"Failed to generate URL for {cache_key}: {e}")
                self._url_cache[cache_key] = None
        return self._url_cache[cache_key]
    
    def _get_redirects_url_pattern_name(self, action):
        """
        Generate the correct URL pattern name for redirects actions
        
        Args:
            action: The action (index, add, edit, delete)
            
        Returns:
            String URL pattern name (e.g., 'wagtailredirects:index')
        """
        return f"wagtailredirects:{action}"
    
    def get_redirects_index_url(self):
        """
        Get the main redirects index URL
        
        Returns:
            String URL or None if not available
        """
        try:
            cache_key = "redirects_index"
            url_pattern = self._get_redirects_url_pattern_name('index')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating redirects index URL: {e}")
        
        return None
    
    def get_redirect_add_url(self):
        """
        Get the add redirect URL
        
        Returns:
            String URL or None if not available
        """
        try:
            cache_key = "redirect_add"
            url_pattern = self._get_redirects_url_pattern_name('add')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating redirect add URL: {e}")
        
        return None
    
    def get_redirect_edit_url(self, redirect_id):
        """
        Get the edit URL for a specific redirect
        
        Args:
            redirect_id: The ID of the redirect
            
        Returns:
            String URL or None if not available
        """
        if not redirect_id:
            return None
        
        try:
            cache_key = f"redirect_edit_{redirect_id}"
            url_pattern = self._get_redirects_url_pattern_name('edit')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern,
                args=[redirect_id]
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating redirect edit URL for redirect {redirect_id}: {e}")
        
        return None
    
    def get_redirect_delete_url(self, redirect_id):
        """
        Get the delete URL for a specific redirect
        
        Args:
            redirect_id: The ID of the redirect
            
        Returns:
            String URL or None if not available
        """
        if not redirect_id:
            return None
        
        try:
            cache_key = f"redirect_delete_{redirect_id}"
            url_pattern = self._get_redirects_url_pattern_name('delete')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern,
                args=[redirect_id]
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating redirect delete URL for redirect {redirect_id}: {e}")
        
        return None
    
    def get_all_redirect_urls(self, redirect_id):
        """
        Get all available admin URLs for a redirect
        
        Args:
            redirect_id: The ID of the redirect
            
        Returns:
            Dict of URL types to URLs
        """
        if not redirect_id:
            return {}
            
        urls = {}
        url_methods = {
            'edit': self.get_redirect_edit_url,
            'delete': self.get_redirect_delete_url,
        }
        
        for url_type, method in url_methods.items():
            url = method(redirect_id)
            if url:
                urls[url_type] = url
                
        return urls
    
    def clear_cache(self):
        """
        Clear the URL cache
        """
        self._url_cache.clear()


def get_redirects():
    """
    Get redirect objects with basic information
    
    Returns:
        List of tuples (redirect_id, old_path, redirect_to, is_permanent)
    """
    redirects = []
    try:
        for redirect in Redirect.objects.all().order_by('old_path'):
            redirect_to = redirect.redirect_page.url if redirect.redirect_page else redirect.redirect_link
            redirects.append((
                redirect.id,
                redirect.old_path,
                redirect_to,
                redirect.is_permanent
            ))
    except Redirect.DoesNotExist:
        logger.error("Error fetching redirects: Redirect model not found")
    
    return redirects


def get_redirects_urls(output, base_url, max_instances, user=None):
    """
    Generate comprehensive URLs for Wagtail redirects functionality
    
    Args:
        output: StringIO object for logging
        base_url: Base URL for the site
        max_instances: Maximum number of redirect instances to process
        user: User object for permission checking
        
    Returns:
        List of tuples (model_name, url_type, full_url)
    """
    urls = []
    
    # Initialize the enhanced admin URL finder with user context
    url_finder = RedirectsAdminURLFinder(user)
    
    # Get the Redirect model name
    redirect_model_name = f"{Redirect._meta.app_label}.{Redirect.__name__}"
    
    output.write("Processing Redirects functionality\n")
    
    # Get redirects index URL
    redirects_index_url = url_finder.get_redirects_index_url()
    if redirects_index_url:
        urls.append((redirect_model_name, "index", f"{base_url}{redirects_index_url}"))
    
    # Get add redirect URL
    redirect_add_url = url_finder.get_redirect_add_url()
    if redirect_add_url:
        urls.append((redirect_model_name, "add", f"{base_url}{redirect_add_url}"))
    
    # Get existing redirects
    redirects = get_redirects()
    output.write(f"Found {len(redirects)} redirects\n")
    
    # Limit the number of redirects processed
    limited_redirects = redirects[:max_instances]
    
    for redirect_id, old_path, redirect_to, is_permanent in limited_redirects:
        output.write(f"Processing redirect: {old_path} -> {redirect_to} (ID: {redirect_id})\n")
        
        # Create a model identifier that includes the redirect info
        redirect_instance_model_name = f"{redirect_model_name}_Instance_{redirect_id}"
        
        # Get all available admin URLs for this redirect
        all_urls = url_finder.get_all_redirect_urls(redirect_id)
        
        # Add each URL type to our results
        for url_type, url in all_urls.items():
            urls.append((redirect_instance_model_name, url_type, f"{base_url}{url}"))
    
    output.write(f"Generated {len(urls)} redirect URLs\n")
    return urls
