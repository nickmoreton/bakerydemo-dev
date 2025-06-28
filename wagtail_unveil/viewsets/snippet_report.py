from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.snippets.models import get_snippet_models




def get_snippet_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, full_url) for snippets
    urls = []
    snippet_models = get_snippet_models()
    for model in snippet_models:
        model_name = f"{model._meta.app_label}.{model.__name__}"
        # Add URL
        try:
            url_pattern = f"wagtailsnippets_{model._meta.app_label}_{model._meta.model_name}:add"
            add_url = reverse(url_pattern)
            urls.append((model_name, 'add', f"{base_url}{add_url}"))
        except NoReverseMatch:
            pass
        # List URL
        try:
            url_pattern = f"wagtailsnippets_{model._meta.app_label}_{model._meta.model_name}:list"
            list_url = reverse(url_pattern)
            urls.append((model_name, 'list', f"{base_url}{list_url}"))
        except NoReverseMatch:
            pass
        try:
            instances = model.objects.all()[:max_instances] if max_instances else model.objects.all()
            for instance in instances:
                snippet_model_name = f"{model._meta.app_label}.{model.__name__}_{instance.id}_{getattr(instance, 'title', getattr(instance, 'name', str(instance)))}"
                # Edit URL
                try:
                    url_pattern = f"wagtailsnippets_{model._meta.app_label}_{model._meta.model_name}:edit"
                    edit_url = reverse(url_pattern, args=[instance.pk])
                    urls.append((snippet_model_name, 'edit', f"{base_url}{edit_url}"))
                except NoReverseMatch:
                    pass
                # Delete URL
                try:
                    url_pattern = f"wagtailsnippets_{model._meta.app_label}_{model._meta.model_name}:delete"
                    delete_url = reverse(url_pattern, args=[instance.pk])
                    urls.append((snippet_model_name, 'delete', f"{base_url}{delete_url}"))
                except NoReverseMatch:
                    pass
                # Copy URL
                try:
                    url_pattern = f"wagtailsnippets_{model._meta.app_label}_{model._meta.model_name}:copy"
                    copy_url = reverse(url_pattern, args=[instance.pk])
                    urls.append((snippet_model_name, 'copy', f"{base_url}{copy_url}"))
                except NoReverseMatch:
                    pass
                # History URL
                try:
                    url_pattern = f"wagtailsnippets_{model._meta.app_label}_{model._meta.model_name}:history"
                    history_url = reverse(url_pattern, args=[instance.pk])
                    urls.append((snippet_model_name, 'history', f"{base_url}{history_url}"))
                except NoReverseMatch:
                    pass
                # Usage URL
                try:
                    url_pattern = f"wagtailsnippets_{model._meta.app_label}_{model._meta.model_name}:usage"
                    usage_url = reverse(url_pattern, args=[instance.pk])
                    urls.append((snippet_model_name, 'usage', f"{base_url}{usage_url}"))
                except NoReverseMatch:
                    pass
        except (model.DoesNotExist, AttributeError, ValueError, TypeError):
            pass
    return urls


class UnveilSnippetReportIndexView(IndexView):
    # Index view for the Snippet Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Snippet"
    header_icon = "sliders"
    paginate_by = None

    def get_queryset(self):
        # Get the queryset for snippet URLs
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        snippet_urls = get_snippet_urls(base_url, max_instances)
        for model_name, url_type, url in snippet_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls

    def get_header_buttons(self):
        # Get header buttons
        return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={"data-action": "check-urls"},
            )
        ]


class UnveilSnippetReportViewSet(ViewSet):
    # ViewSet for Unveil Snippet reports
    icon = "sliders"
    menu_label = "Snippet"
    menu_name = "unveil_snippet_report"
    url_namespace = "unveil_snippet_report"
    url_prefix = "unveil/snippet-report"
    index_view_class = UnveilSnippetReportIndexView
    
    def get_urlpatterns(self):
        # Return the URL patterns for this ViewSet
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


# Create an instance of the ViewSet to be registered
unveil_snippet_viewset = UnveilSnippetReportViewSet("unveil_snippet_report")
