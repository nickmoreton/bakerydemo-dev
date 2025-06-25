import logging

from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch, reverse
from wagtail.admin.admin_url_finder import ModelAdminURLFinder
from wagtail.models import Page, get_page_models
from wagtail.permission_policies import ModelPermissionPolicy

logger = logging.getLogger(__name__)


class PageAdminURLFinder(ModelAdminURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail Page models.
    Provides comprehensive URL generation with permission checking and error handling.
    """
    
    def __init__(self, user=None):
        """
        Initialize with optional user for permission checking
        """
        super().__init__(user)
        self._url_cache = {}
        self.permission_policy = ModelPermissionPolicy(Page)
    
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
    
    def get_add_url(self, model, parent=None):
        """
        Get the add URL for creating a new page of the given model type
        
        Args:
            model: The Page model class
            parent: Optional parent page instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not model or not issubclass(model, Page):
            return None
            
        # Check permissions if user is provided
        if self.user and not self.permission_policy.user_has_permission(self.user, 'add'):
            return None
            
        try:
            if parent:
                cache_key = f"add_{model._meta.label_lower}_{parent.pk}"
                return self._get_cached_url(
                    cache_key,
                    reverse,
                    'wagtailadmin_pages:add',
                    args=[model._meta.app_label, model._meta.model_name, parent.pk]
                )
            else:
                # Try to get a default parent (root page)
                root_page = Page.objects.filter(depth=1).first()
                if root_page:
                    return self.get_add_url(model, root_page)
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating add URL for {model}: {e}")
        
        return None

    def get_edit_url(self, instance):
        """
        Get the edit URL for the given page instance
        
        Args:
            instance: Page instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance or not isinstance(instance, Page):
            return None
            
        # Check permissions if user is provided
        if (self.user and 
            not self.permission_policy.user_has_permission_for_instance(
                self.user, 'change', instance
            )):
            return None
            
        cache_key = f"edit_{instance._meta.label_lower}_{instance.pk}"
        return self._get_cached_url(
            cache_key,
            reverse,
            'wagtailadmin_pages:edit',
            args=[instance.pk]
        )

    def get_delete_url(self, instance):
        """
        Get the delete URL for the given page instance
        
        Args:
            instance: Page instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance or not isinstance(instance, Page):
            return None
            
        # Check permissions if user is provided
        if (self.user and 
            not self.permission_policy.user_has_permission_for_instance(
                self.user, 'delete', instance
            )):
            return None
            
        cache_key = f"delete_{instance._meta.label_lower}_{instance.pk}"
        return self._get_cached_url(
            cache_key,
            reverse,
            'wagtailadmin_pages:delete',
            args=[instance.pk]
        )
    
    def get_copy_url(self, instance):
        """
        Get the copy URL for the given page instance
        """
        if not instance or not isinstance(instance, Page):
            return None
            
        if (self.user and 
            not self.permission_policy.user_has_permission_for_instance(
                self.user, 'add', instance
            )):
            return None
            
        cache_key = f"copy_{instance._meta.label_lower}_{instance.pk}"
        return self._get_cached_url(
            cache_key,
            reverse,
            'wagtailadmin_pages:copy',
            args=[instance.pk]
        )
    
    def get_move_url(self, instance):
        """
        Get the move URL for the given page instance
        """
        if not instance or not isinstance(instance, Page):
            return None
            
        if (self.user and 
            not self.permission_policy.user_has_permission_for_instance(
                self.user, 'change', instance
            )):
            return None
            
        cache_key = f"move_{instance._meta.label_lower}_{instance.pk}"
        return self._get_cached_url(
            cache_key,
            reverse,
            'wagtailadmin_pages:move',
            args=[instance.pk]
        )
    
    def get_revisions_url(self, instance):
        """
        Get the revisions URL for the given page instance
        """
        if not instance or not isinstance(instance, Page):
            return None
            
        cache_key = f"revisions_{instance._meta.label_lower}_{instance.pk}"
        return self._get_cached_url(
            cache_key,
            reverse,
            'wagtailadmin_pages:revisions_index',
            args=[instance.pk]
        )
    
    def get_history_url(self, instance):
        """
        Get the history URL for the given page instance
        """
        if not instance or not isinstance(instance, Page):
            return None
            
        cache_key = f"history_{instance._meta.label_lower}_{instance.pk}"
        return self._get_cached_url(
            cache_key,
            reverse,
            'wagtailadmin_pages:history',
            args=[instance.pk]
        )
    
    def get_view_draft_url(self, instance):
        """
        Get the view draft URL for the given page instance
        """
        if not instance or not isinstance(instance, Page):
            return None
            
        cache_key = f"view_draft_{instance._meta.label_lower}_{instance.pk}"
        return self._get_cached_url(
            cache_key,
            reverse,
            'wagtailadmin_pages:view_draft',
            args=[instance.pk]
        )
    
    def get_workflow_history_url(self, instance):
        """
        Get the workflow history URL for the given page instance
        """
        if not instance or not isinstance(instance, Page):
            return None
            
        cache_key = f"workflow_history_{instance._meta.label_lower}_{instance.pk}"
        return self._get_cached_url(
            cache_key,
            reverse,
            'wagtailadmin_pages:workflow_history',
            args=[instance.pk]
        )
    
    def get_all_urls(self, instance):
        """
        Get all available admin URLs for a page instance
        
        Returns:
            Dict of URL types to URLs
        """
        if not instance or not isinstance(instance, Page):
            return {}
            
        urls = {}
        url_methods = {
            'edit': self.get_edit_url,
            'delete': self.get_delete_url,
            'copy': self.get_copy_url,
            'move': self.get_move_url,
            'revisions': self.get_revisions_url,
            'history': self.get_history_url,
            'view_draft': self.get_view_draft_url,
            'workflow_history': self.get_workflow_history_url,
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


def get_page_urls(output, base_url, max_instances=1, user=None):
    """
    Generate URLs for all Wagtail Page models using enhanced AdminURLFinder.
    
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
    url_finder = PageAdminURLFinder(user)
    
    # Get all Page models using Wagtail's utility function
    page_models = get_page_models()
    
    output.write(f"Found {len(page_models)} Page models\n")
    
    for model in page_models:
        # Exclude the base Page model as it's not a concrete page type
        if model._meta.label_lower == 'wagtailcore.page':
            continue
            
        model_name = f"{model._meta.app_label}.{model.__name__}"
        
        # Get root page for add URLs
        root_page = Page.objects.filter(depth=1).first()
        if root_page:
            # Get add URL using enhanced AdminURLFinder with parent page
            add_url = url_finder.get_add_url(model, parent=root_page)
            if add_url:
                urls.append((model_name, "add", f"{base_url}{add_url}"))
        
        # Get existing instances and create URLs for them
        try:
            instances = model.objects.live()[:max_instances]
            output.write(f"Found {instances.count()} live instances for {model_name}\n")
        except AttributeError:
            # Handle cases where the model doesn't have a 'live' manager
            instances = model.objects.all()[:max_instances]
            output.write(f"Found {len(instances)} instances for {model_name}\n")
        
        for instance in instances:
            # Get all available admin URLs for this instance
            all_urls = url_finder.get_all_urls(instance)
            
            # Add each URL type to our results
            for url_type, url in all_urls.items():
                urls.append((model_name, url_type, f"{base_url}{url}"))
            
            # View URL (front-end) - not an admin URL but useful
            if hasattr(instance, 'url') and instance.url:
                view_url = instance.url
                if not view_url.startswith('http'):
                    # Ensure we have a proper URL structure
                    if view_url.startswith('/'):
                        view_url = f"{base_url}{view_url}"
                    else:
                        view_url = f"{base_url}/{view_url}"
                urls.append((model_name, "view", view_url))
                
    output.write(f"Generated {len(urls)} page URLs\n")
    return urls
