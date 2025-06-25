import logging

from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch, reverse
from wagtail.admin.admin_url_finder import ModelAdminURLFinder
from wagtail.models import Site

logger = logging.getLogger(__name__)


class SiteAdminURLFinder(ModelAdminURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail Site models.
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
    
    def _get_url_pattern_name(self, action):
        """
        Generate the correct URL pattern name for site actions
        
        Args:
            action: The action (add, index, edit, delete)
            
        Returns:
            String URL pattern name (e.g., 'wagtailsites:add')
        """
        return f"wagtailsites:{action}"

    def get_add_url(self):
        """
        Get the add URL for creating a new site
        
        Returns:
            String URL or None if not available/permitted
        """
        try:
            cache_key = "add_site"
            url_pattern = self._get_url_pattern_name('add')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating add URL for sites: {e}")
        
        return None

    def get_index_url(self):
        """
        Get the index/list URL for sites
        
        Returns:
            String URL or None if not available
        """
        try:
            cache_key = "index_site"
            url_pattern = self._get_url_pattern_name('index')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating index URL for sites: {e}")
        
        return None

    def get_edit_url(self, instance):
        """
        Get the edit URL for the given site instance
        
        Args:
            instance: Site instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        cache_key = f"edit_site_{instance.pk}"
        url_pattern = self._get_url_pattern_name('edit')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )

    def get_delete_url(self, instance):
        """
        Get the delete URL for the given site instance
        
        Args:
            instance: Site instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        cache_key = f"delete_site_{instance.pk}"
        url_pattern = self._get_url_pattern_name('delete')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    def get_frontend_url(self, instance):
        """
        Get the frontend URL for the given site instance
        
        Args:
            instance: Site instance
            
        Returns:
            String URL representing the actual site frontend
        """
        if not instance:
            return None
        
        # Build the frontend URL from site hostname and port
        protocol = "https" if instance.port == 443 else "http"
        if instance.port in [80, 443]:
            return f"{protocol}://{instance.hostname}/"
        else:
            return f"{protocol}://{instance.hostname}:{instance.port}/"
    
    def get_all_urls(self, instance):
        """
        Get all available admin URLs for a site instance
        
        Returns:
            Dict of URL types to URLs
        """
        if not instance:
            return {}
            
        urls = {}
        url_methods = {
            'edit': self.get_edit_url,
            'delete': self.get_delete_url,
            'frontend': self.get_frontend_url,  # Special case: actual site URL
        }
        
        for url_type, method in url_methods.items():
            url = method(instance)
            if url:
                urls[url_type] = url
                
        return urls
    
    def clear_cache(self):
        """
        Clear the internal URL cache
        """
        self._url_cache.clear()


def get_site_urls(output, base_url, max_instances=10, user=None):
    """
    Generate URLs for Wagtail Site models using enhanced AdminURLFinder.
    
    Args:
        output: StringIO object for logging/debugging output
        base_url: Base URL for the site (e.g., "http://localhost:8000") - for admin URLs
        max_instances: Maximum number of instance URLs to generate per model
        user: Optional user for permission checking
        
    Returns:
        List of tuples: (model_name, url_type, url)
    """
    urls = []
    
    # Initialize the enhanced admin URL finder with user context
    url_finder = SiteAdminURLFinder(user)
    
    # Get the site model
    model_name = f"{Site._meta.app_label}.{Site.__name__}"
    
    output.write(f"Processing Site model: {model_name}\n")
    
    # Get add URL for the model
    add_url = url_finder.get_add_url()
    if add_url:
        urls.append((model_name, "add", f"{base_url}{add_url}"))
    
    # Get index URL for the model
    index_url = url_finder.get_index_url()
    if index_url:
        urls.append((model_name, "index", f"{base_url}{index_url}"))
    
    # Get existing instances and create URLs for them
    try:
        instances = Site.objects.all()[:max_instances]
        output.write(f"Found {len(instances)} site instances\n")
    except (AttributeError, ValueError, TypeError) as e:
        output.write(f"Error getting site instances: {e}\n")
        return urls
    
    for instance in instances:
        # Get all available admin URLs for this instance
        all_urls = url_finder.get_all_urls(instance)
        
        # Add each URL type to our results
        for url_type, url in all_urls.items():
            if url_type == 'frontend':
                # Frontend URLs don't need base_url prefix as they're complete URLs
                urls.append((model_name, url_type, url))
            else:
                # Admin URLs need base_url prefix
                urls.append((model_name, url_type, f"{base_url}{url}"))
            
    output.write(f"Generated {len(urls)} site URLs\n")
    return urls
