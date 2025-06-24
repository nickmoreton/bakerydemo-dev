import logging

from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch, reverse
from wagtail.admin.admin_url_finder import ModelAdminURLFinder
from wagtail.snippets.models import get_snippet_models

logger = logging.getLogger(__name__)


class SnippetAdminURLFinder(ModelAdminURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail Snippet models.
    Provides comprehensive URL generation with permission checking and error handling.
    """
    
    # URL patterns will be generated dynamically based on model
    # Format: wagtailsnippets_{app_label}_{model_name}:{action}
    
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
    
    def _get_url_pattern_name(self, model, action):
        """
        Generate the correct URL pattern name for a snippet model and action
        
        Args:
            model: The snippet model class
            action: The action (add, list, edit, delete, copy, history, usage)
            
        Returns:
            String URL pattern name (e.g., 'wagtailsnippets_breads_breadingredient:list')
        """
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        return f"wagtailsnippets_{app_label}_{model_name}:{action}"
    
    def get_add_url(self, model):
        """
        Get the add URL for creating a new snippet of the given model type
        
        Args:
            model: The snippet model class
            
        Returns:
            String URL or None if not available/permitted
        """
        if not model:
            return None
        
        try:
            cache_key = f"add_{model._meta.label_lower}"
            url_pattern = self._get_url_pattern_name(model, 'add')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating add URL for {model}: {e}")
        
        return None
    
    def get_list_url(self, model):
        """
        Get the list URL for the given snippet model
        
        Args:
            model: The snippet model class
            
        Returns:
            String URL or None if not available
        """
        if not model:
            return None

        try:
            cache_key = f"list_{model._meta.label_lower}"
            url_pattern = self._get_url_pattern_name(model, 'list')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating list URL for {model}: {e}")
        
        return None

    def get_edit_url(self, instance):
        """
        Get the edit URL for the given snippet instance
        
        Args:
            instance: Snippet instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        model = type(instance)
        cache_key = f"edit_{model._meta.label_lower}_{instance.pk}"
        url_pattern = self._get_url_pattern_name(model, 'edit')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )

    def get_delete_url(self, instance):
        """
        Get the delete URL for the given snippet instance
        
        Args:
            instance: Snippet instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        model = type(instance)
        cache_key = f"delete_{model._meta.label_lower}_{instance.pk}"
        url_pattern = self._get_url_pattern_name(model, 'delete')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    def get_copy_url(self, instance):
        """
        Get the copy URL for the given snippet instance
        """
        if not instance:
            return None
        
        model = type(instance)
        cache_key = f"copy_{model._meta.label_lower}_{instance.pk}"
        url_pattern = self._get_url_pattern_name(model, 'copy')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    def get_history_url(self, instance):
        """
        Get the history URL for the given snippet instance
        """
        if not instance:
            return None
        
        model = type(instance)
        cache_key = f"history_{model._meta.label_lower}_{instance.pk}"
        url_pattern = self._get_url_pattern_name(model, 'history')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    def get_usage_url(self, instance):
        """
        Get the usage URL for the given snippet instance
        """
        if not instance:
            return None
        
        model = type(instance)
        cache_key = f"usage_{model._meta.label_lower}_{instance.pk}"
        url_pattern = self._get_url_pattern_name(model, 'usage')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    def get_all_urls(self, instance):
        """
        Get all available admin URLs for a snippet instance
        
        Returns:
            Dict of URL types to URLs
        """
        if not instance:
            return {}
            
        urls = {}
        url_methods = {
            'edit': self.get_edit_url,
            'delete': self.get_delete_url,
            'copy': self.get_copy_url,
            'history': self.get_history_url,
            'usage': self.get_usage_url,
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


def get_snippet_urls(output, base_url, max_instances=1, user=None):
    """
    Generate URLs for all Wagtail Snippet models using enhanced AdminURLFinder.
    
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
    url_finder = SnippetAdminURLFinder(user)
    
    # Get all snippet models using Wagtail's utility function
    snippet_models = get_snippet_models()
    
    output.write(f"Found {len(snippet_models)} Snippet models\n")
    
    for model in snippet_models:
        model_name = f"{model._meta.app_label}.{model.__name__}"
        
        # Get add URL for the model
        add_url = url_finder.get_add_url(model)
        if add_url:
            urls.append((model_name, "add", f"{base_url}{add_url}"))
        
        # Get list URL for the model
        list_url = url_finder.get_list_url(model)
        if list_url:
            urls.append((model_name, "list", f"{base_url}{list_url}"))
        
        # Get existing instances and create URLs for them
        try:
            instances = model.objects.all()[:max_instances]
            output.write(f"Found {len(instances)} instances for {model_name}\n")
        except (AttributeError, ValueError, TypeError) as e:
            output.write(f"Error getting instances for {model_name}: {e}\n")
            continue
        
        for instance in instances:
            # Get all available admin URLs for this instance
            all_urls = url_finder.get_all_urls(instance)
            
            # Add each URL type to our results
            for url_type, url in all_urls.items():
                urls.append((model_name, url_type, f"{base_url}{url}"))
                
    output.write(f"Generated {len(urls)} snippet URLs\n")
    return urls
