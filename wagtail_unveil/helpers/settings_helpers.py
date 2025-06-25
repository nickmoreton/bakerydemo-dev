import logging

from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch, reverse
from wagtail.admin.admin_url_finder import ModelAdminURLFinder
from wagtail.contrib.settings import registry
from wagtail.contrib.settings.models import BaseSiteSetting

logger = logging.getLogger(__name__)


class SettingsAdminURLFinder(ModelAdminURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail Settings.
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
    
    def _get_settings_url_pattern_name(self, model, action, site_pk=None):
        """
        Generate the correct URL pattern name for settings actions
        
        Args:
            model: The settings model
            action: The action (edit)
            site_pk: The site primary key (optional)
            
        Returns:
            String URL pattern name (e.g., 'wagtailsettings:edit')
        """
        return f"wagtailsettings:{action}"
    
    def get_settings_edit_url(self, model, site_pk=None):
        """
        Get the edit URL for a specific settings model
        
        Args:
            model: The settings model class
            site_pk: The site primary key (optional)
            
        Returns:
            String URL or None if not available
        """
        try:
            cache_key = f"settings_edit_{model._meta.label}_{site_pk or 'default'}"
            url_pattern = self._get_settings_url_pattern_name(model, 'edit', site_pk)
            
            # Build URL arguments
            args = [model._meta.app_label, model._meta.model_name]
            if site_pk:
                args.append(site_pk)
            
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern,
                args=args
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating settings edit URL for {model._meta.label}: {e}")
        
        return None
    
    def get_all_settings_urls(self, model, site_pk=None):
        """
        Get all available admin URLs for a settings model
        
        Args:
            model: The settings model class
            site_pk: The site primary key (optional)
            
        Returns:
            Dict of URL types to URLs
        """
        urls = {}
        
        # Get edit URL
        edit_url = self.get_settings_edit_url(model, site_pk)
        if edit_url:
            urls['edit'] = edit_url
                
        return urls
    
    def clear_cache(self):
        """
        Clear the URL cache
        """
        self._url_cache.clear()


def get_settings_models():
    """
    Get all registered settings models by scanning all Django models that inherit from BaseSiteSetting
    
    Returns:
        List of tuples (model_class, model_name, app_label)
    """
    settings_models = []
    try:
        # Get all models from all apps
        for model in apps.get_models():
            # Check if the model inherits from BaseSiteSetting
            if issubclass(model, BaseSiteSetting):
                settings_models.append((
                    model,
                    model._meta.model_name,
                    model._meta.app_label
                ))
                logger.info(f"Found settings model: {model._meta.app_label}.{model._meta.model_name}")
                        
    except (AttributeError, TypeError, ValueError) as e:
        logger.error(f"Error fetching settings models: {e}")
        # Debug: Let's see what attributes the registry actually has
        logger.error(f"Registry attributes: {dir(registry)}")
    
    return settings_models


def get_settings_instances():
    """
    Get all existing settings instances across all sites and models
    
    Returns:
        List of tuples (model_class, instance_id, site_id, site_hostname, model_name)
    """
    instances = []
    try:
        settings_models = get_settings_models()
        logger.info(f"Found {len(settings_models)} registered settings models")
        
        for model_class, model_name, app_label in settings_models:
            logger.info(f"Checking model: {app_label}.{model_name}")
            
            # Check if this is a multi-site settings model
            is_multisite = hasattr(model_class, 'site')
            logger.info(f"  Is multisite: {is_multisite}")
            
            if is_multisite:
                # Get instances for each site
                instance_count = model_class.objects.count()
                logger.info(f"  Found {instance_count} instances")
                
                for instance in model_class.objects.select_related('site').all():
                    logger.info(f"  Adding instance ID {instance.id} for site {instance.site.hostname}")
                    instances.append((
                        model_class,
                        instance.id,
                        instance.site.id,
                        instance.site.hostname,
                        model_name
                    ))
            else:
                # Single-site settings - get all instances
                instance_count = model_class.objects.count()
                logger.info(f"  Found {instance_count} instances")
                
                for instance in model_class.objects.all():
                    logger.info(f"  Adding instance ID {instance.id}")
                    instances.append((
                        model_class,
                        instance.id,
                        None,  # No site for single-site settings
                        'default',  # Default hostname
                        model_name
                    ))
                    
    except (AttributeError, ValueError) as e:
        logger.error(f"Error fetching settings instances: {e}")
    
    logger.info(f"Total instances found: {len(instances)}")
    return instances


def get_available_sites():
    """
    Get available sites for multi-site settings
    
    Returns:
        List of tuples (site_id, site_hostname, site_name)
    """
    from wagtail.models import Site
    
    sites = []
    try:
        for site in Site.objects.all():
            sites.append((
                site.id,
                site.hostname,
                site.site_name or f"Site {site.id}"
            ))
    except Site.DoesNotExist as e:
        logger.error(f"Error fetching sites: {e}")
    
    return sites


def get_settings_urls(output, base_url, max_instances, user=None):
    """
    Generate comprehensive URLs for Wagtail settings functionality
    
    Args:
        output: StringIO object for logging
        base_url: Base URL for the site
        max_instances: Maximum number of setting instances to process
        user: User object for permission checking
        
    Returns:
        List of tuples (model_name, url_type, full_url)
    """
    urls = []
    
    # Initialize the enhanced admin URL finder with user context
    url_finder = SettingsAdminURLFinder(user)
    
    output.write("Processing Settings functionality\n")
    
    # Get all existing settings instances
    settings_instances = get_settings_instances()
    output.write(f"Found {len(settings_instances)} settings instances\n")
    
    if settings_instances:
        # Process actual instances
        limited_instances = settings_instances[:max_instances]
        
        for model_class, instance_id, site_id, site_hostname, model_name in limited_instances:
            app_label = model_class._meta.app_label
            
            if site_id:
                output.write(f"Processing settings instance: {app_label}.{model_name} for site {site_hostname} (ID: {instance_id})\n")
                # Create a site-specific model identifier
                settings_model_name = f"{app_label}.{model_class.__name__}_Site_{site_id}_Instance_{instance_id}"
                
                # Get all available admin URLs for this settings instance
                all_urls = url_finder.get_all_settings_urls(model_class, site_id)
            else:
                output.write(f"Processing settings instance: {app_label}.{model_name} (ID: {instance_id})\n")
                # Create a model identifier for single-site settings
                settings_model_name = f"{app_label}.{model_class.__name__}_Instance_{instance_id}"
                
                # Get all available admin URLs for this settings instance
                all_urls = url_finder.get_all_settings_urls(model_class)
            
            # Add each URL type to our results
            for url_type, url in all_urls.items():
                urls.append((settings_model_name, url_type, f"{base_url}{url}"))
    else:
        # Fallback: Generate URLs for all registered models and sites
        output.write("No settings instances found, generating URLs for all registered models\n")
        
        settings_models = get_settings_models()
        sites = get_available_sites()
        
        for model_class, model_name, app_label in settings_models[:max_instances]:
            output.write(f"Processing settings model: {app_label}.{model_name}\n")
            
            # Check if this is a multi-site settings model
            is_multisite = hasattr(model_class, 'site')
            
            if is_multisite:
                # Generate URLs for each site
                for site_id, site_hostname, site_name in sites:
                    output.write(f"  Processing for site: {site_hostname} (ID: {site_id})\n")
                    
                    # Create a site-specific model identifier
                    settings_model_name = f"{app_label}.{model_class.__name__}_Site_{site_id}"
                    
                    # Get all available admin URLs for this settings model and site
                    all_urls = url_finder.get_all_settings_urls(model_class, site_id)
                    
                    # Add each URL type to our results
                    for url_type, url in all_urls.items():
                        urls.append((settings_model_name, url_type, f"{base_url}{url}"))
            else:
                # Single-site settings model
                output.write("  Processing as single-site settings\n")
                
                # Create a model identifier
                settings_model_name = f"{app_label}.{model_class.__name__}"
                
                # Get all available admin URLs for this settings model
                all_urls = url_finder.get_all_settings_urls(model_class)
                
                # Add each URL type to our results
                for url_type, url in all_urls.items():
                    urls.append((settings_model_name, url_type, f"{base_url}{url}"))
    
    output.write(f"Generated {len(urls)} settings URLs\n")
    return urls
