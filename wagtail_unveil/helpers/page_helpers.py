from django.urls import reverse
from wagtail.models import Page, get_page_models
from wagtail.admin.admin_url_finder import AdminURLFinder


class PageAdminURLFinder(AdminURLFinder):
    """
    Custom Admin URL Finder for Wagtail to generate URLs for all Page models.
    This extends the default AdminURLFinder to include additional functionality.
    """

    def get_add_url(self, model, parent=None):
        """
        Get the add URL for creating a new page of the given model type
        """
        if parent:
            return reverse('wagtailadmin_pages:add', args=[
                model._meta.app_label,
                model._meta.model_name,
                parent.pk
            ])
        return None

    def get_delete_url(self, instance):
        """
        Get the delete URL for the given page instance
        """
        return reverse('wagtailadmin_pages:delete', args=[instance.pk])


def get_page_urls(output, base_url, max_instances=1):
    """
    Generate URLs for all Wagtail Page models using AdminURLFinder.
    
    Args:
        output: StringIO object for logging/debugging output
        base_url: Base URL for the site (e.g., "http://localhost:8000")
        max_instances: Maximum number of instance URLs to generate per model
        
    Returns:
        List of tuples: (model_name, url_type, url)
    """
    urls = []
    
    # Initialize the admin URL finder
    url_finder = PageAdminURLFinder()
    
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
            # Get add URL using AdminURLFinder with parent page
            add_url = url_finder.get_add_url(model, parent=root_page)
            if add_url:
                urls.append((model_name, "add", f"{base_url}{add_url}"))
        
        # Get existing instances and create URLs for them
        instances = model.objects.live()[:max_instances]
        output.write(f"Found {instances.count()} live instances for {model_name}\n")
        
        for instance in instances:
            # Edit URL using AdminURLFinder
            edit_url = url_finder.get_edit_url(instance)
            if edit_url:
                urls.append((model_name, "edit", f"{base_url}{edit_url}"))
            
            # View URL (front-end)
            if hasattr(instance, 'url') and instance.url:
                view_url = instance.url
                if not view_url.startswith('http'):
                    # Ensure we have a proper URL structure
                    if view_url.startswith('/'):
                        view_url = f"{base_url}{view_url}"
                    else:
                        view_url = f"{base_url}/{view_url}"
                urls.append((model_name, "view", view_url))
            
            # Delete URL using AdminURLFinder
            delete_url = url_finder.get_delete_url(instance)
            if delete_url:
                urls.append((model_name, "delete", f"{base_url}{delete_url}"))
                
    output.write(f"Generated {len(urls)} page URLs\n")
    return urls
