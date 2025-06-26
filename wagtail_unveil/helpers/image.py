import logging

from django.urls import reverse
from wagtail.images import get_image_model

from .base import UnveilURLFinder

logger = logging.getLogger(__name__)


class ImageAdminURLFinder(UnveilURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail Image models.
    Provides comprehensive URL generation with permission checking and error handling.
    """
    
    def _get_url_pattern_name(self, action):
        """
        Generate the correct URL pattern name for image actions
        
        Args:
            action: The action (add, index, edit, delete, copy, usage)
            
        Returns:
            String URL pattern name (e.g., 'wagtailimages:add')
        """
        return f"wagtailimages:{action}"

    def get_add_url(self):
        """
        Get the add URL for creating a new image
        
        Returns:
            String URL or None if not available/permitted
        """
        cache_key = "add_image"
        url_pattern = self._get_url_pattern_name('add')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern
        )

    def get_index_url(self):
        """
        Get the index/list URL for images
        
        Returns:
            String URL or None if not available
        """
        cache_key = "index_image"
        url_pattern = self._get_url_pattern_name('index')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern
        )

    def get_edit_url(self, instance):
        """
        Get the edit URL for the given image instance
        
        Args:
            instance: Image instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        cache_key = f"edit_image_{instance.pk}"
        url_pattern = self._get_url_pattern_name('edit')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )

    def get_delete_url(self, instance):
        """
        Get the delete URL for the given image instance
        
        Args:
            instance: Image instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        cache_key = f"delete_image_{instance.pk}"
        url_pattern = self._get_url_pattern_name('delete')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    def get_copy_url(self, instance):
        """
        Get the copy URL for the given image instance
        """
        if not instance:
            return None
        
        cache_key = f"copy_image_{instance.pk}"
        url_pattern = self._get_url_pattern_name('copy')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    def get_usage_url(self, instance):
        """
        Get the usage URL for the given image instance
        """
        if not instance:
            return None
        
        cache_key = f"usage_image_{instance.pk}"
        url_pattern = self._get_url_pattern_name('usage')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    def get_all_urls(self, instance):
        """
        Get all available admin URLs for an image instance
        
        Returns:
            Dict of URL types to URLs
        """
        if not instance:
            return {}
            
        urls = {}
        url_methods = {
            'edit': self.get_edit_url,
            'delete': self.get_delete_url,
            # Note: copy and usage URLs are not available for images in Wagtail
        }
        
        for url_type, method in url_methods.items():
            url = method(instance)
            if url:
                urls[url_type] = url
                
        return urls


def get_image_urls(output, base_url, max_instances=1, user=None):
    """
    Generate URLs for Wagtail Image models using enhanced AdminURLFinder.
    
    Args:
        output: StringIO object for logging/debugging output
        base_url: Base URL for the site (e.g., "http://localhost:8000")
        max_instances: Maximum number of instance URLs to generate per model
        user: Optional user for permission checking
        
    Returns:
        List of tuples: (model_name, url_type, url)
    """
    urls = []
    
    # Initialize the enhanced admin URL finder with user context
    url_finder = ImageAdminURLFinder(user)
    
    # Get the image model
    ImageModel = get_image_model()
    model_name = f"{ImageModel._meta.app_label}.{ImageModel.__name__}"
    
    output.write(f"Processing Image model: {model_name}\n")
    
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
        instances = ImageModel.objects.all()[:max_instances]
        output.write(f"Found {len(instances)} image instances\n")
    except (AttributeError, ValueError, TypeError) as e:
        output.write(f"Error getting image instances: {e}\n")
        return urls
    
    for instance in instances:
        # Get all available admin URLs for this instance
        all_urls = url_finder.get_all_urls(instance)
        
        # Add each URL type to our results
        for url_type, url in all_urls.items():
            urls.append((model_name, url_type, f"{base_url}{url}"))
            
    output.write(f"Generated {len(urls)} image URLs\n")
    return urls
