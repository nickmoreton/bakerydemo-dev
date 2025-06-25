import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from .base import UnveilURLFinder

logger = logging.getLogger(__name__)


class UserAdminURLFinder(UnveilURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail User and Group models.
    Provides comprehensive URL generation with permission checking and error handling.
    """
    
    def _get_user_url_pattern_name(self, action):
        """
        Generate the correct URL pattern name for user actions
        
        Args:
            action: The action (add, index, edit, delete)
            
        Returns:
            String URL pattern name (e.g., 'wagtailusers_users:add')
        """
        return f"wagtailusers_users:{action}"
    
    def _get_group_url_pattern_name(self, action):
        """
        Generate the correct URL pattern name for group actions
        
        Args:
            action: The action (add, index, edit, delete)
            
        Returns:
            String URL pattern name (e.g., 'wagtailusers_groups:add')
        """
        return f"wagtailusers_groups:{action}"

    # User URL methods
    def get_user_add_url(self):
        """
        Get the add URL for creating a new user
        
        Returns:
            String URL or None if not available/permitted
        """
        cache_key = "add_user"
        url_pattern = self._get_user_url_pattern_name('add')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern
        )

    def get_user_index_url(self):
        """
        Get the index/list URL for users
        
        Returns:
            String URL or None if not available
        """
        cache_key = "index_user"
        url_pattern = self._get_user_url_pattern_name('index')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern
        )

    def get_user_edit_url(self, instance):
        """
        Get the edit URL for the given user instance
        
        Args:
            instance: User instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        cache_key = f"edit_user_{instance.pk}"
        url_pattern = self._get_user_url_pattern_name('edit')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )

    def get_user_delete_url(self, instance):
        """
        Get the delete URL for the given user instance
        
        Args:
            instance: User instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        cache_key = f"delete_user_{instance.pk}"
        url_pattern = self._get_user_url_pattern_name('delete')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    # Group URL methods
    def get_group_add_url(self):
        """
        Get the add URL for creating a new group
        
        Returns:
            String URL or None if not available/permitted
        """
        cache_key = "add_group"
        url_pattern = self._get_group_url_pattern_name('add')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern
        )

    def get_group_index_url(self):
        """
        Get the index/list URL for groups
        
        Returns:
            String URL or None if not available
        """
        cache_key = "index_group"
        url_pattern = self._get_group_url_pattern_name('index')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern
        )

    def get_group_edit_url(self, instance):
        """
        Get the edit URL for the given group instance
        
        Args:
            instance: Group instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        cache_key = f"edit_group_{instance.pk}"
        url_pattern = self._get_group_url_pattern_name('edit')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )

    def get_group_delete_url(self, instance):
        """
        Get the delete URL for the given group instance
        
        Args:
            instance: Group instance
            
        Returns:
            String URL or None if not available/permitted
        """
        if not instance:
            return None
        
        cache_key = f"delete_group_{instance.pk}"
        url_pattern = self._get_group_url_pattern_name('delete')
        return self._get_cached_url(
            cache_key,
            reverse,
            url_pattern,
            args=[instance.pk]
        )
    
    def get_all_user_urls(self, instance):
        """
        Get all available admin URLs for a user instance
        
        Returns:
            Dict of URL types to URLs
        """
        if not instance:
            return {}
            
        urls = {}
        url_methods = {
            'edit': self.get_user_edit_url,
            'delete': self.get_user_delete_url,
        }
        
        for url_type, method in url_methods.items():
            url = method(instance)
            if url:
                urls[url_type] = url
                
        return urls
    
    def get_all_group_urls(self, instance):
        """
        Get all available admin URLs for a group instance
        
        Returns:
            Dict of URL types to URLs
        """
        if not instance:
            return {}
            
        urls = {}
        url_methods = {
            'edit': self.get_group_edit_url,
            'delete': self.get_group_delete_url,
        }
        
        for url_type, method in url_methods.items():
            url = method(instance)
            if url:
                urls[url_type] = url
                
        return urls


def get_user_urls(output, base_url, max_instances=5, user=None):
    """
    Generate URLs for Wagtail User and Group models using enhanced AdminURLFinder.
    
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
    url_finder = UserAdminURLFinder(user)
    
    # Get the User model
    User = get_user_model()
    user_model_name = f"{User._meta.app_label}.{User.__name__}"
    
    output.write(f"Processing User model: {user_model_name}\n")
    
    # Get user add URL
    user_add_url = url_finder.get_user_add_url()
    if user_add_url:
        urls.append((user_model_name, "add", f"{base_url}{user_add_url}"))
    
    # Get user index URL
    user_index_url = url_finder.get_user_index_url()
    if user_index_url:
        urls.append((user_model_name, "index", f"{base_url}{user_index_url}"))
    
    # Get existing user instances and create URLs for them
    try:
        user_instances = User.objects.all()[:max_instances]
        output.write(f"Found {len(user_instances)} user instances\n")
    except (AttributeError, ValueError, TypeError) as e:
        output.write(f"Error getting user instances: {e}\n")
        user_instances = []
    
    for instance in user_instances:
        # Get all available admin URLs for this user instance
        all_urls = url_finder.get_all_user_urls(instance)
        
        # Add each URL type to our results
        for url_type, url in all_urls.items():
            urls.append((user_model_name, url_type, f"{base_url}{url}"))
    
    # Process Groups
    group_model_name = f"{Group._meta.app_label}.{Group.__name__}"
    
    output.write(f"Processing Group model: {group_model_name}\n")
    
    # Get group add URL
    group_add_url = url_finder.get_group_add_url()
    if group_add_url:
        urls.append((group_model_name, "add", f"{base_url}{group_add_url}"))
    
    # Get group index URL
    group_index_url = url_finder.get_group_index_url()
    if group_index_url:
        urls.append((group_model_name, "index", f"{base_url}{group_index_url}"))
    
    # Get existing group instances and create URLs for them
    try:
        group_instances = Group.objects.all()[:max_instances]
        output.write(f"Found {len(group_instances)} group instances\n")
    except (AttributeError, ValueError, TypeError) as e:
        output.write(f"Error getting group instances: {e}\n")
        group_instances = []
    
    for instance in group_instances:
        # Get all available admin URLs for this group instance
        all_urls = url_finder.get_all_group_urls(instance)
        
        # Add each URL type to our results
        for url_type, url in all_urls.items():
            urls.append((group_model_name, url_type, f"{base_url}{url}"))
            
    output.write(f"Generated {len(urls)} user/group URLs\n")
    return urls
