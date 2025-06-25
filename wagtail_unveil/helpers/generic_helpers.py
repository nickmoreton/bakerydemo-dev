import logging

from django.apps import apps
from django.urls import reverse

from .base import UnveilURLFinder

logger = logging.getLogger(__name__)


class GenericModelAdminURLFinder(UnveilURLFinder):
    """
    Enhanced Admin URL Finder for generic models managed by ModelViewSet.
    Provides comprehensive URL generation with permission checking and error handling.
    """
    
    def _get_url_pattern_name(self, model, action):
        """
        Generate the correct URL pattern name for a generic model and action
        
        Args:
            model: The model class
            action: The action (add, index, edit, delete, copy, history, usage)
            
        Returns:
            String URL pattern name (e.g., 'country:add')
        """
        model_name = model._meta.model_name
        return f"{model_name}:{action}"
    
    def get_add_url(self, model):
        """
        Get the add URL for creating a new instance of the given model type
        
        Args:
            model: The model class
            
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
        Get the list URL for the given model
        
        Args:
            model: The model class
            
        Returns:
            String URL or None if not available
        """
        if not model:
            return None

        try:
            cache_key = f"list_{model._meta.label_lower}"
            url_pattern = self._get_url_pattern_name(model, 'index')  # ModelViewSet uses 'index' not 'list'
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
        Get the edit URL for the given instance
        
        Args:
            instance: Model instance
            
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
        Get the delete URL for the given instance
        
        Args:
            instance: Model instance
            
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
        Get the copy URL for the given instance
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
        Get the history URL for the given instance
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
        Get the usage URL for the given instance
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
        Get all available admin URLs for an instance
        
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


def get_generic_models():
    """
    Get all models that should be included in the generic report.
    This reads from Django settings to get the list of models to include.
    
    Returns:
        List of model classes
    """
    from django.conf import settings
    
    # Get the list of models from settings
    generic_models_list = getattr(settings, 'WAGTAIL_UNVEIL_GENERIC_MODELS', [
        'bakerydemo.breads.Country',
    ])
    
    models = []
    for model_path in generic_models_list:
        try:
            app_label, model_name = model_path.rsplit('.', 1)
            model = apps.get_model(app_label, model_name)
            models.append(model)
            logger.info(f"Found generic model: {model_path}")
        except (LookupError, ValueError) as e:
            logger.error(f"Error loading model {model_path}: {e}")
    
    return models


def get_generic_urls(output, base_url, max_instances=1, user=None):
    """
    Generate URLs for all generic models using enhanced AdminURLFinder.
    
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
    url_finder = GenericModelAdminURLFinder(user)
    
    # Get all generic models from settings
    generic_models = get_generic_models()
    
    output.write(f"Found {len(generic_models)} Generic models\n")
    
    for model in generic_models:
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
                
    output.write(f"Generated {len(urls)} generic model URLs\n")
    return urls
