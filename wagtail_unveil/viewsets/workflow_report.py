from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.viewsets.base import ViewSet
from wagtail.models import Workflow

from wagtail_unveil.models import UrlEntry
from wagtail_unveil.viewsets.base import UnveilReportView


def get_workflow_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, full_url) for workflows
    urls = []
    
    # Add index and add URLs
    try:
        index_url = reverse('wagtailadmin_workflows:index')
        urls.append(('wagtail.Workflow', 'index', f"{base_url}{index_url}"))
    except NoReverseMatch:
        pass
    try:
        add_url = reverse('wagtailadmin_workflows:add')
        urls.append(('wagtail.Workflow', 'add', f"{base_url}{add_url}"))
    except NoReverseMatch:
        pass
    
    try:
        workflows = Workflow.objects.all()[:max_instances] if max_instances else Workflow.objects.all()
        for workflow in workflows:
            workflow_model_name = f"wagtail.Workflow ({workflow.name})"
            # Admin URLs
            try:
                edit_url = reverse('wagtailadmin_workflows:edit', args=[workflow.id])
                urls.append((workflow_model_name, 'edit', f"{base_url}{edit_url}"))
            except NoReverseMatch:
                pass
            try:
                delete_url = reverse('wagtailadmin_workflows:delete', args=[workflow.id])
                urls.append((workflow_model_name, 'delete', f"{base_url}{delete_url}"))
            except NoReverseMatch:
                pass
            try:
                copy_url = reverse('wagtailadmin_workflows:copy', args=[workflow.id])
                urls.append((workflow_model_name, 'copy', f"{base_url}{copy_url}"))
            except NoReverseMatch:
                pass
            try:
                usage_url = reverse('wagtailadmin_workflows:usage', args=[workflow.id])
                urls.append((workflow_model_name, 'usage', f"{base_url}{usage_url}"))
            except NoReverseMatch:
                pass
    except Workflow.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilWorkflowReportIndexView(UnveilReportView):
    # Index view for the Workflow Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Workflow"
    header_icon = "tasks"
    paginate_by = None

    def get_queryset(self):
        # Get the queryset for workflow URLs
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
        workflow_urls = get_workflow_urls(base_url, max_instances)
        for model_name, url_type, url in workflow_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilWorkflowReportViewSet(ViewSet):
    # ViewSet for Unveil Workflow reports
    icon = "tasks"
    menu_label = "Workflow"
    menu_name = "unveil_workflow_report"
    url_namespace = "unveil_workflow_report"
    url_prefix = "unveil/workflow-report"
    index_view_class = UnveilWorkflowReportIndexView
    
    def get_urlpatterns(self):
        # Return the URL patterns for this ViewSet
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


# Create an instance of the ViewSet to be registered
unveil_workflow_viewset = UnveilWorkflowReportViewSet("unveil_workflow_report") 