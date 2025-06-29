from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.viewsets.base import ViewSet
from wagtail.models import Task

from wagtail_unveil.models import UrlEntry
from wagtail_unveil.viewsets.base import UnveilReportView, UnveilReportViewSet


def get_workflow_task_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, full_url) for workflow tasks
    urls = []
    
    # Add index and add URLs for tasks
    try:
        index_url = reverse('wagtailadmin_workflows:task_index')
        urls.append(('wagtail.Task', 'index', f"{base_url}{index_url}"))
    except NoReverseMatch:
        pass
    try:
        add_url = reverse('wagtailadmin_workflows:select_task_type')
        urls.append(('wagtail.Task', 'add', f"{base_url}{add_url}"))
    except NoReverseMatch:
        pass
    
    try:
        tasks = Task.objects.all()[:max_instances] if max_instances else Task.objects.all()
        for task in tasks:
            task_model_name = f"wagtail.Task ({task.name})"
            # Admin URLs
            try:
                edit_url = reverse('wagtailadmin_workflows:edit_task', args=[task.id])
                urls.append((task_model_name, 'edit', f"{base_url}{edit_url}"))
            except NoReverseMatch:
                pass
            try:
                delete_url = reverse('wagtailadmin_workflows:delete_task', args=[task.id])
                urls.append((task_model_name, 'delete', f"{base_url}{delete_url}"))
            except NoReverseMatch:
                pass
            try:
                usage_url = reverse('wagtailadmin_workflows:task_usage', args=[task.id])
                urls.append((task_model_name, 'usage', f"{base_url}{usage_url}"))
            except NoReverseMatch:
                pass
    except Task.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilWorkflowTaskReportIndexView(UnveilReportView):
    # Index view for the Workflow Task Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Workflow Task"
    header_icon = "thumbtack"
    paginate_by = None

    def get_queryset(self):
        # Get the queryset for workflow task URLs
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
        task_urls = get_workflow_task_urls(base_url, max_instances)
        for model_name, url_type, url in task_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilWorkflowTaskReportViewSet(UnveilReportViewSet):
    # ViewSet for Unveil Workflow Task reports
    icon = "thumbtack"
    menu_label = "Workflow Task"
    menu_name = "unveil_workflow_task_report"
    url_namespace = "unveil_workflow_task_report"
    url_prefix = "unveil/workflow-task-report"
    index_view_class = UnveilWorkflowTaskReportIndexView
    



# Create an instance of the ViewSet to be registered
unveil_workflow_task_viewset = UnveilWorkflowTaskReportViewSet("unveil_workflow_task_report") 