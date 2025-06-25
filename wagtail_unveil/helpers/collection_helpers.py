import logging

from django.urls import NoReverseMatch, reverse
from wagtail.admin.admin_url_finder import ModelAdminURLFinder
from wagtail.models import Collection

logger = logging.getLogger(__name__)


class CollectionAdminURLFinder(ModelAdminURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail Collections.
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
            except (NoReverseMatch, AttributeError) as e:
                logger.warning(f"Failed to generate URL for {cache_key}: {e}")
                self._url_cache[cache_key] = None
        return self._url_cache[cache_key]
    
    def get_collection_index_url(self):
        """
        Get the collections index URL
        
        Returns:
            String URL or None if not available
        """
        try:
            return self._get_cached_url(
                'collection_index',
                reverse,
                'wagtailadmin_collections:index'
            )
        except (NoReverseMatch, AttributeError) as e:
            logger.error(f"Error generating collection index URL: {e}")
        
        return None
    
    def get_collection_add_url(self):
        """
        Get the collection add URL
        
        Returns:
            String URL or None if not available
        """
        try:
            return self._get_cached_url(
                'collection_add',
                reverse,
                'wagtailadmin_collections:add'
            )
        except (NoReverseMatch, AttributeError) as e:
            logger.error(f"Error generating collection add URL: {e}")
        
        return None
    
    def get_collection_edit_url(self, collection_id):
        """
        Get the edit URL for a specific collection
        
        Args:
            collection_id: The collection ID
            
        Returns:
            String URL or None if not available
        """
        try:
            cache_key = f"collection_edit_{collection_id}"
            return self._get_cached_url(
                cache_key,
                reverse,
                'wagtailadmin_collections:edit',
                args=[collection_id]
            )
        except (NoReverseMatch, AttributeError) as e:
            logger.error(f"Error generating collection edit URL for ID {collection_id}: {e}")
        
        return None
    
    def get_collection_delete_url(self, collection_id):
        """
        Get the delete URL for a specific collection
        
        Args:
            collection_id: The collection ID
            
        Returns:
            String URL or None if not available
        """
        try:
            cache_key = f"collection_delete_{collection_id}"
            return self._get_cached_url(
                cache_key,
                reverse,
                'wagtailadmin_collections:delete',
                args=[collection_id]
            )
        except (NoReverseMatch, AttributeError) as e:
            logger.error(f"Error generating collection delete URL for ID {collection_id}: {e}")
        
        return None
    
    def get_all_collection_urls(self, collection_id):
        """
        Get all available admin URLs for a collection
        
        Args:
            collection_id: The collection ID
            
        Returns:
            Dict of URL types to URLs
        """
        urls = {}
        
        # Get edit URL
        edit_url = self.get_collection_edit_url(collection_id)
        if edit_url:
            urls['edit'] = edit_url
        
        # Get delete URL
        delete_url = self.get_collection_delete_url(collection_id)
        if delete_url:
            urls['delete'] = delete_url
        
        return urls
    
    def clear_cache(self):
        """
        Clear the URL cache
        """
        self._url_cache.clear()


def get_collection_urls(output, base_url, max_instances, user=None):
    """
    Generate comprehensive URLs for Wagtail collections functionality
    
    Args:
        output: StringIO object for logging
        base_url: Base URL for the site
        max_instances: Maximum number of collection instances to process
        user: User object for permission checking
        
    Returns:
        List of tuples (model_name, url_type, full_url)
    """
    urls = []
    
    # Initialize the enhanced admin URL finder with user context
    url_finder = CollectionAdminURLFinder(user)
    
    output.write("Processing Collections functionality\n")
    
    # Add collection management URLs
    # Index URL
    index_url = url_finder.get_collection_index_url()
    if index_url:
        urls.append(('wagtail.Collection', 'index', f"{base_url}{index_url}"))
    
    # Add URL
    add_url = url_finder.get_collection_add_url()
    if add_url:
        urls.append(('wagtail.Collection', 'add', f"{base_url}{add_url}"))
    
    # Get existing collections (excluding root collection)
    try:
        # Exclude the root collection as it's not useful for admin operations
        collections = Collection.objects.exclude(depth=1)[:max_instances]
        output.write(f"Found {collections.count()} collections (excluding root)\n")
        
        for collection in collections:
            output.write(f"Processing collection: {collection.name} (ID: {collection.id})\n")
            
            # Create a collection identifier
            collection_model_name = f"wagtail.Collection_{collection.id}_{collection.name}"
            
            # Get all available admin URLs for this collection
            all_urls = url_finder.get_all_collection_urls(collection.id)
            
            # Add each URL type to our results
            for url_type, url in all_urls.items():
                urls.append((collection_model_name, url_type, f"{base_url}{url}"))
                
    except Collection.DoesNotExist as e:
        output.write(f"No collections found: {e}\n")
    except (AttributeError, ValueError, TypeError) as e:
        output.write(f"Error processing collections: {e}\n")
        logger.error(f"Error processing collections: {e}")
    
    output.write(f"Generated {len(urls)} collection URLs\n")
    return urls
