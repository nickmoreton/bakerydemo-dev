from collections import namedtuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import NoReverseMatch, reverse, path
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton


def get_user_add_url():
    """Get the add URL for creating a new user."""
    try:
        return reverse('wagtailusers_users:add')
    except NoReverseMatch:
        return None


def get_user_index_url():
    """Get the index/list URL for users."""
    try:
        return reverse('wagtailusers_users:index')
    except NoReverseMatch:
        return None


def get_user_edit_url(instance):
    """Get the edit URL for the given user instance."""
    if not instance:
        return None
    try:
        return reverse('wagtailusers_users:edit', args=[instance.pk])
    except NoReverseMatch:
        return None


def get_user_delete_url(instance):
    """Get the delete URL for the given user instance."""
    if not instance:
        return None
    try:
        return reverse('wagtailusers_users:delete', args=[instance.pk])
    except NoReverseMatch:
        return None


def get_group_add_url():
    """Get the add URL for creating a new group."""
    try:
        return reverse('wagtailusers_groups:add')
    except NoReverseMatch:
        return None


def get_group_index_url():
    """Get the index/list URL for groups."""
    try:
        return reverse('wagtailusers_groups:index')
    except NoReverseMatch:
        return None


def get_group_edit_url(instance):
    """Get the edit URL for the given group instance."""
    if not instance:
        return None
    try:
        return reverse('wagtailusers_groups:edit', args=[instance.pk])
    except NoReverseMatch:
        return None


def get_group_delete_url(instance):
    """Get the delete URL for the given group instance."""
    if not instance:
        return None
    try:
        return reverse('wagtailusers_groups:delete', args=[instance.pk])
    except NoReverseMatch:
        return None


def get_user_urls(base_url, max_instances=5):
    """
    Generate URLs for Wagtail User and Group models.
    
    Args:
        base_url: Base URL for the site (e.g., "http://localhost:8000")
        max_instances: Maximum number of instance URLs to generate per model
        
    Returns:
        List of tuples: (model_name, url_type, url)
    """
    urls = []
    
    # Get the User model
    User = get_user_model()
    user_model_name = f"{User._meta.app_label}.{User.__name__}"
    
    # Get user add URL
    user_add_url = get_user_add_url()
    if user_add_url:
        urls.append((user_model_name, "add", f"{base_url}{user_add_url}"))
    
    # Get user index URL
    user_index_url = get_user_index_url()
    if user_index_url:
        urls.append((user_model_name, "index", f"{base_url}{user_index_url}"))
    
    # Get existing user instances and create URLs for them
    try:
        user_instances = User.objects.all()
        if max_instances:
            user_instances = user_instances[:max_instances]
    except Exception:
        user_instances = []
    
    for instance in user_instances:
        # Get edit URL
        edit_url = get_user_edit_url(instance)
        if edit_url:
            urls.append((user_model_name, "edit", f"{base_url}{edit_url}"))
        
        # Get delete URL
        delete_url = get_user_delete_url(instance)
        if delete_url:
            urls.append((user_model_name, "delete", f"{base_url}{delete_url}"))
    
    # Process Groups
    group_model_name = f"{Group._meta.app_label}.{Group.__name__}"
    
    # Get group add URL
    group_add_url = get_group_add_url()
    if group_add_url:
        urls.append((group_model_name, "add", f"{base_url}{group_add_url}"))
    
    # Get group index URL
    group_index_url = get_group_index_url()
    if group_index_url:
        urls.append((group_model_name, "index", f"{base_url}{group_index_url}"))
    
    # Get existing group instances and create URLs for them
    try:
        group_instances = Group.objects.all()
        if max_instances:
            group_instances = group_instances[:max_instances]
    except Exception:
        group_instances = []
    
    for instance in group_instances:
        # Get edit URL
        edit_url = get_group_edit_url(instance)
        if edit_url:
            urls.append((group_model_name, "edit", f"{base_url}{edit_url}"))
        
        # Get delete URL
        delete_url = get_group_delete_url(instance)
        if delete_url:
            urls.append((group_model_name, "delete", f"{base_url}{delete_url}"))
            
    return urls


class UnveilUserReportIndexView(IndexView):
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil User "
    header_icon = "user"
    paginate_by = None

    def get_queryset(self):
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        user_urls = get_user_urls(base_url, max_instances)
        for model_name, url_type, url in user_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
        return all_urls

    def get_header_buttons(self):
        return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={"data-action": "check-urls"},
            )
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        return context


class UnveilUserReportViewSet(ViewSet):
    model = None
    icon = "user"
    menu_label = "User"
    menu_name = "unveil_user_report"
    url_namespace = "unveil_user_report"
    url_prefix = "unveil/user-report"
    index_view_class = UnveilUserReportIndexView

    def get_urlpatterns(self):
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


unveil_user_viewset = UnveilUserReportViewSet("unveil_user_report")
