from django.apps import apps
from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.viewsets.base import ViewSet

from wagtail_unveil.models import UrlEntry
from wagtail_unveil.viewsets.base import UnveilReportView, UnveilReportViewSet


def get_generic_models():
    # Get all models for the generic report
    # Get the list of models from settings
    generic_models_list = getattr(settings, 'WAGTAIL_UNVEIL_GENERIC_MODELS', [])
    
    models = []
    for model_path in generic_models_list:
        try:
            app_label, model_name = model_path.rsplit('.', 1)
            model = apps.get_model(app_label, model_name)
            models.append(model)
        except (LookupError, ValueError):
            continue
    
    return models


def get_generic_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, url) for generic models
    urls = []
    generic_models = get_generic_models()
    for model in generic_models:
        model_name = f"{model._meta.app_label}.{model.__name__}"
        # Add URL
        try:
            add_url = reverse(f"{model._meta.model_name}:add")
            urls.append((model_name, "add", f"{base_url}{add_url}"))
        except NoReverseMatch:
            pass
        # List URL
        try:
            list_url = reverse(f"{model._meta.model_name}:index")
            urls.append((model_name, "list", f"{base_url}{list_url}"))
        except NoReverseMatch:
            pass
        # Instances
        try:
            instances = model.objects.all()
            if max_instances:
                instances = instances[:max_instances]
        except (model.DoesNotExist, AttributeError, ValueError, TypeError):
            continue
        for instance in instances:
            # Edit URL
            try:
                edit_url = reverse(f"{model._meta.model_name}:edit", args=[instance.pk])
                urls.append((model_name, "edit", f"{base_url}{edit_url}"))
            except NoReverseMatch:
                pass
            # Delete URL
            try:
                delete_url = reverse(f"{model._meta.model_name}:delete", args=[instance.pk])
                urls.append((model_name, "delete", f"{base_url}{delete_url}"))
            except NoReverseMatch:
                pass
            # Copy URL
            try:
                copy_url = reverse(f"{model._meta.model_name}:copy", args=[instance.pk])
                urls.append((model_name, "copy", f"{base_url}{copy_url}"))
            except NoReverseMatch:
                pass
            # History URL
            try:
                history_url = reverse(f"{model._meta.model_name}:history", args=[instance.pk])
                urls.append((model_name, "history", f"{base_url}{history_url}"))
            except NoReverseMatch:
                pass
            # Usage URL
            try:
                usage_url = reverse(f"{model._meta.model_name}:usage", args=[instance.pk])
                urls.append((model_name, "usage", f"{base_url}{usage_url}"))
            except NoReverseMatch:
                pass
    return urls


class UnveilGenericReportIndexView(UnveilReportView):
    # Index view for the Generic Model Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Generic Model "
    header_icon = "table"
    paginate_by = None

    def get_queryset(self):
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
        generic_urls = get_generic_urls(base_url, max_instances)
        for model_name, url_type, url in generic_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
        return all_urls

class UnveilGenericReportViewSet(UnveilReportViewSet):
    # ViewSet for Unveil Generic Model reports
    model = None
    icon = "table"
    menu_label = "Generic Model"
    menu_name = "unveil_generic_report"
    url_namespace = "unveil_generic_report"
    url_prefix = "unveil/generic-report"
    index_view_class = UnveilGenericReportIndexView



unveil_generic_viewset = UnveilGenericReportViewSet("unveil_generic_report")
