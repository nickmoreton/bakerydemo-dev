import logging

from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch, reverse
from wagtail.admin.admin_url_finder import ModelAdminURLFinder
from wagtail.contrib.search_promotions.models import SearchPromotion

logger = logging.getLogger(__name__)


class SearchPromotionsAdminURLFinder(ModelAdminURLFinder):
    """
    Enhanced Admin URL Finder for Wagtail Search Promotions.
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
    
    def _get_search_promotions_url_pattern_name(self, action):
        """
        Generate the correct URL pattern name for search promotions actions
        
        Args:
            action: The action (index, add, edit, delete)
            
        Returns:
            String URL pattern name (e.g., 'wagtailsearchpromotions:index')
        """
        return f"wagtailsearchpromotions:{action}"
    
    def get_search_promotions_index_url(self):
        """
        Get the main search promotions index URL
        
        Returns:
            String URL or None if not available
        """
        try:
            cache_key = "search_promotions_index"
            url_pattern = self._get_search_promotions_url_pattern_name('index')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating search promotions index URL: {e}")
        
        return None
    
    def get_search_promotion_add_url(self):
        """
        Get the add search promotion URL
        
        Returns:
            String URL or None if not available
        """
        try:
            cache_key = "search_promotion_add"
            url_pattern = self._get_search_promotions_url_pattern_name('add')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating search promotion add URL: {e}")
        
        return None
    
    def get_search_promotion_edit_url(self, promotion_id):
        """
        Get the edit URL for a specific search promotion
        
        Args:
            promotion_id: The ID of the search promotion
            
        Returns:
            String URL or None if not available
        """
        if not promotion_id:
            return None
        
        try:
            cache_key = f"search_promotion_edit_{promotion_id}"
            url_pattern = self._get_search_promotions_url_pattern_name('edit')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern,
                args=[promotion_id]
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating search promotion edit URL for promotion {promotion_id}: {e}")
        
        return None
    
    def get_search_promotion_delete_url(self, promotion_id):
        """
        Get the delete URL for a specific search promotion
        
        Args:
            promotion_id: The ID of the search promotion
            
        Returns:
            String URL or None if not available
        """
        if not promotion_id:
            return None
        
        try:
            cache_key = f"search_promotion_delete_{promotion_id}"
            url_pattern = self._get_search_promotions_url_pattern_name('delete')
            return self._get_cached_url(
                cache_key,
                reverse,
                url_pattern,
                args=[promotion_id]
            )
        except (NoReverseMatch, ImproperlyConfigured, AttributeError) as e:
            logger.error(f"Error generating search promotion delete URL for promotion {promotion_id}: {e}")
        
        return None
    
    def get_all_search_promotion_urls(self, promotion_id):
        """
        Get all available admin URLs for a search promotion
        
        Args:
            promotion_id: The ID of the search promotion
            
        Returns:
            Dict of URL types to URLs
        """
        if not promotion_id:
            return {}
            
        urls = {}
        url_methods = {
            'edit': self.get_search_promotion_edit_url,
            'delete': self.get_search_promotion_delete_url,
        }
        
        for url_type, method in url_methods.items():
            url = method(promotion_id)
            if url:
                urls[url_type] = url
                
        return urls
    
    def clear_cache(self):
        """
        Clear the URL cache
        """
        self._url_cache.clear()


def get_search_promotions():
    """
    Get search promotion objects with basic information
    
    Returns:
        List of tuples (promotion_id, query, description, page_title)
    """
    promotions = []
    try:
        for promotion in SearchPromotion.objects.all().order_by('query'):
            page_title = promotion.page.title if promotion.page else "No page"
            promotions.append((
                promotion.id,
                promotion.query,
                promotion.description,
                page_title
            ))
    except SearchPromotion.DoesNotExist:
        logger.error("Error fetching search promotions: SearchPromotion model not found")
    
    return promotions


def get_search_promotions_urls(output, base_url, max_instances, user=None):
    """
    Generate comprehensive URLs for Wagtail search promotions functionality
    
    Args:
        output: StringIO object for logging
        base_url: Base URL for the site
        max_instances: Maximum number of search promotion instances to process
        user: User object for permission checking
        
    Returns:
        List of tuples (model_name, url_type, full_url)
    """
    urls = []
    
    # Initialize the enhanced admin URL finder with user context
    url_finder = SearchPromotionsAdminURLFinder(user)
    
    # Get the SearchPromotion model name
    search_promotion_model_name = f"{SearchPromotion._meta.app_label}.{SearchPromotion.__name__}"
    
    output.write("Processing Search Promotions functionality\n")
    
    # Get search promotions index URL
    search_promotions_index_url = url_finder.get_search_promotions_index_url()
    if search_promotions_index_url:
        urls.append((search_promotion_model_name, "index", f"{base_url}{search_promotions_index_url}"))
    
    # Get add search promotion URL
    search_promotion_add_url = url_finder.get_search_promotion_add_url()
    if search_promotion_add_url:
        urls.append((search_promotion_model_name, "add", f"{base_url}{search_promotion_add_url}"))
    
    # Get existing search promotions
    promotions = get_search_promotions()
    output.write(f"Found {len(promotions)} search promotions\n")
    
    # Limit the number of search promotions processed
    limited_promotions = promotions[:max_instances]
    
    for promotion_id, query, description, page_title in limited_promotions:
        output.write(f"Processing search promotion: {query} -> {page_title} (ID: {promotion_id})\n")
        
        # Create a model identifier that includes the promotion info
        promotion_instance_model_name = f"{search_promotion_model_name}_Instance_{promotion_id}"
        
        # Get all available admin URLs for this search promotion
        all_urls = url_finder.get_all_search_promotion_urls(promotion_id)
        
        # Add each URL type to our results
        for url_type, url in all_urls.items():
            urls.append((promotion_instance_model_name, url_type, f"{base_url}{url}"))
    
    output.write(f"Generated {len(urls)} search promotion URLs\n")
    return urls
