import logging

from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch, reverse
from wagtail.admin.admin_url_finder import ModelAdminURLFinder
from wagtail.models import Locale

logger = logging.getLogger(__name__)


class LocaleAdminURLFinder(ModelAdminURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail Locale models.
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
    
    def _get_locale_url_pattern_name(self, action):
        """
        Generate the correct URL pattern name for locale actions
        
        Args:
            action: The action (add, index, edit, delete)
            
        Returns:
            String URL pattern name (e.g., 'wagtaillocales:add')
        """
        return f"wagtaillocales:{action}"
    
    def get_locale_add_url(self):
        """
        Get the add URL for creating a new locale
        
        Returns:
            String URL or None if not available/permitted
        """
        try:
            cache_key = "add_locale"
            url_pattern = self._get_locale_url_pattern_name('add')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating add URL for locales: {e}")
        
        return None

    def get_locale_index_url(self):
        """
        Get the index/list URL for locales
        
        Returns:
            String URL or None if not available
        """
        try:
            cache_key = "index_locale"
            url_pattern = self._get_locale_url_pattern_name('index')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating index URL for locales: {e}")
        
        return None

    def get_locale_edit_url(self, instance):
        """
        Get the edit URL for the given locale instance
        
        Args:
            instance: Locale instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        cache_key = f"edit_locale_{instance.pk}"
        url_pattern = self._get_locale_url_pattern_name('edit')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )

    def get_locale_delete_url(self, instance):
        """
        Get the delete URL for the given locale instance
        
        Args:
            instance: Locale instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        cache_key = f"delete_locale_{instance.pk}"
        url_pattern = self._get_locale_url_pattern_name('delete')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    def get_all_locale_urls(self, instance):
        """
        Get all available admin URLs for a locale instance
        
        Returns:
            Dict of URL types to URLs
        """
        if not instance:
            return {}
            
        urls = {}
        url_methods = {
            'edit': self.get_locale_edit_url,
            'delete': self.get_locale_delete_url,
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


def get_locale_urls(output, base_url, max_instances=10, user=None):
    """
    Generate URLs for Wagtail Locale models using enhanced AdminURLFinder.
    
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
    url_finder = LocaleAdminURLFinder(user)
    
    # Get the Locale model
    locale_model_name = f"{Locale._meta.app_label}.{Locale.__name__}"
    
    output.write(f"Processing Locale model: {locale_model_name}\n")
    
    # Get locale add URL
    locale_add_url = url_finder.get_locale_add_url()
    if locale_add_url:
        urls.append((locale_model_name, "add", f"{base_url}{locale_add_url}"))
    
    # Get locale index URL
    locale_index_url = url_finder.get_locale_index_url()
    if locale_index_url:
        urls.append((locale_model_name, "index", f"{base_url}{locale_index_url}"))
    
    # Get existing locale instances and create URLs for them
    try:
        locale_instances = Locale.objects.all()[:max_instances]
        output.write(f"Found {len(locale_instances)} locale instances\n")
    except (AttributeError, ValueError, TypeError) as e:
        output.write(f"Error getting locale instances: {e}\n")
        locale_instances = []
    
    for instance in locale_instances:
        # Get all available admin URLs for this locale instance
        all_urls = url_finder.get_all_locale_urls(instance)
        
        # Add each URL type to our results
        for url_type, url in all_urls.items():
            urls.append((locale_model_name, url_type, f"{base_url}{url}"))
    
    output.write(f"Generated {len(urls)} locale URLs\n")
    return urls
