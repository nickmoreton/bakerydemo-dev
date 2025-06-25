"""
Base class for all Wagtail Unveil URL finders.

This module provides a common base class that consolidates shared functionality
across all URL finder helpers, reducing code duplication and providing a 
consistent interface.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple

from django.contrib.auth.models import User
from wagtail.admin.admin_url_finder import ModelAdminURLFinder

logger = logging.getLogger(__name__)


class UnveilURLFinder(ModelAdminURLFinder):
    """
    Base class for all Wagtail Unveil URL finders.
    
    Provides common functionality including:
    - URL caching
    - Error handling
    - Logging
    - Consistent interface for subclasses
    """
    
    def __init__(self, user: Optional[User] = None):
        """
        Initialize the URL finder with a user context.
        
        Args:
            user: The Django user for permission checking (optional)
        """
        super().__init__(user)
        self.user = user
        self._url_cache: Dict[str, Any] = {}
    
    def _get_cached_url(self, cache_key: str, url_generator_func, *args, **kwargs) -> Optional[str]:
        """
        Get a cached URL or generate and cache it if not found.
        
        Args:
            cache_key: Unique key for caching this URL
            url_generator_func: Function to generate the URL if not cached
            *args: Arguments to pass to the URL generator function
            **kwargs: Keyword arguments to pass to the URL generator function
            
        Returns:
            The generated URL or None if generation failed
        """
        if cache_key not in self._url_cache:
            try:
                self._url_cache[cache_key] = url_generator_func(*args, **kwargs)
            except (AttributeError, ImportError, TypeError, ValueError) as e:
                logger.debug(
                    f"Failed to generate URL for cache key '{cache_key}': {e}",
                    exc_info=True
                )
                self._url_cache[cache_key] = None
        
        return self._url_cache[cache_key]
    
    def clear_cache(self) -> None:
        """Clear the URL cache."""
        self._url_cache.clear()
    
    def _log_url_generation_error(self, context: str, error: Exception) -> None:
        """
        Log URL generation errors with consistent formatting.
        
        Args:
            context: Description of what URL was being generated
            error: The exception that occurred
        """
        logger.debug(f"Failed to generate URL for {context}: {error}", exc_info=True)
    
    def _safe_url_generation(self, url_generator_func, context: str, *args, **kwargs) -> Optional[str]:
        """
        Safely generate a URL with error handling and logging.
        
        Args:
            url_generator_func: Function to generate the URL
            context: Description for logging purposes
            *args: Arguments to pass to the URL generator function
            **kwargs: Keyword arguments to pass to the URL generator function
            
        Returns:
            The generated URL or None if generation failed
        """
        try:
            return url_generator_func(*args, **kwargs)
        except (AttributeError, ImportError, TypeError, ValueError) as e:
            self._log_url_generation_error(context, e)
            return None
    
    def get_urls(self, *args, **kwargs) -> List[Tuple[str, str]]:
        """
        Generate URLs for the specific content type.
        
        This method should be implemented by subclasses to provide
        the specific URL generation logic for their content type.
        
        Returns:
            List of tuples containing (URL, description) pairs
        """
        raise NotImplementedError("Subclasses must implement get_urls method")
    
    def _format_url_tuple(self, url: Optional[str], description: str) -> Tuple[str, str]:
        """
        Format a URL tuple with consistent handling of None URLs.
        
        Args:
            url: The URL (may be None)
            description: Description of the URL
            
        Returns:
            Tuple of (url_string, description)
        """
        return (url or "URL not available", description)


def get_unveil_urls(finder_class, user: User, *args, **kwargs) -> List[Tuple[str, str]]:
    """
    Helper function to get URLs from any UnveilURLFinder subclass.
    
    Args:
        finder_class: The UnveilURLFinder subclass to use
        user: The Django user for permission checking
        *args: Arguments to pass to the finder's get_urls method
        **kwargs: Keyword arguments to pass to the finder's get_urls method
        
    Returns:
        List of tuples containing (URL, description) pairs
    """
    if not issubclass(finder_class, UnveilURLFinder):
        raise ValueError(f"{finder_class} must be a subclass of UnveilURLFinder")
    
    finder = finder_class(user)
    return finder.get_urls(*args, **kwargs)
