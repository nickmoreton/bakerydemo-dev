from collections import namedtuple

from django.apps import apps
from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.contrib.settings.models import BaseSiteSetting, BaseGenericSetting


def get_settings_edit_url(app_label, model_name, site_pk=None):
    """Get the edit URL for a specific settings model."""
    try:
        args = [app_label, model_name]
        if site_pk:
            args.append(site_pk)
        return reverse('wagtailsettings:edit', args=args)
    except NoReverseMatch:
        return None


def get_settings_urls(base_url, max_instances):
    """Return a list of tuples (model_name, url_type, full_url) for settings."""
    urls = []
    
    try:
        # Get all settings models
        settings_models = []
        for model in apps.get_models():
            if issubclass(model, (BaseGenericSetting, BaseSiteSetting)):
                settings_models.append(model)
        
        # Process each settings model
        for model_class in settings_models:
            app_label = model_class._meta.app_label
            model_name = model_class._meta.model_name
            
            # Check if this is a multi-site settings model
            is_multisite = hasattr(model_class, 'site')
            
            if is_multisite:
                # Get instances for each site
                try:
                    instances = model_class.objects.select_related('site').all()
                    if max_instances is not None:
                        instances = instances[:max_instances]
                    
                    for instance in instances:
                        settings_model_name = f"{app_label}.{model_class.__name__} (Site Instance)"
                        edit_url = get_settings_edit_url(app_label, model_name, instance.site.id)
                        if edit_url:
                            urls.append((settings_model_name, 'edit', f"{base_url}{edit_url}"))
                except model_class.DoesNotExist:
                    pass
            else:
                # Single-site settings
                try:
                    instances = model_class.objects.all()
                    if max_instances is not None:
                        instances = instances[:max_instances]
                    
                    for instance in instances:
                        settings_model_name = f"{app_label}.{model_class.__name__} (Generic Instance)"
                        edit_url = get_settings_edit_url(app_label, model_name)
                        if edit_url:
                            urls.append((settings_model_name, 'edit', f"{base_url}{edit_url}"))
                except model_class.DoesNotExist:
                    pass
                    
    except (AttributeError, ValueError, TypeError):
        pass
    
    return urls


class UnveilSettingsReportIndexView(IndexView):
    """
    Custom index view for the Settings Report ViewSet.
    """
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Settings"
    header_icon = "cog"
    paginate_by = None

    def get_queryset(self):
        """Generate the queryset for settings URLs."""
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        
        # For settings, we don't limit max_instances since there are typically very few
        # settings models and we want to include all of them (both generic and site-specific)
        max_instances = None  # No limit for settings
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
        settings_urls = get_settings_urls(base_url, max_instances)
        for model_name, url_type, url in settings_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls

    def get_header_buttons(self):
        """Get buttons to display in the header."""
        return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={"data-action": "check-urls"},
            )
        ]


class UnveilSettingsReportViewSet(ViewSet):
    """
    ViewSet for Unveil Settings reports using Wagtail's ViewSet pattern.
    """
    icon = "cogs"
    menu_label = "Settings"
    menu_name = "unveil_settings_report"
    url_namespace = "unveil_settings_report"
    url_prefix = "unveil/settings-report"
    index_view_class = UnveilSettingsReportIndexView
    
    def get_urlpatterns(self):
        """Return the URL patterns for this ViewSet."""
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


# Create an instance of the ViewSet to be registered
unveil_settings_viewset = UnveilSettingsReportViewSet("unveil_settings_report")
