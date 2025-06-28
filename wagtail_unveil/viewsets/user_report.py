from collections import namedtuple

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import NoReverseMatch, reverse, path
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton



def get_user_urls(base_url, max_instances=5):
    """
    Generate URLs for Wagtail User and Group models.
    Returns a list of tuples: (model_name, url_type, url)
    """
    urls = []
    User = get_user_model()
    user_model_name = f"{User._meta.app_label}.{User.__name__}"
    # User add URL
    try:
        user_add_url = reverse('wagtailusers_users:add')
        urls.append((user_model_name, "add", f"{base_url}{user_add_url}"))
    except NoReverseMatch:
        pass
    # User index URL
    try:
        user_index_url = reverse('wagtailusers_users:index')
        urls.append((user_model_name, "index", f"{base_url}{user_index_url}"))
    except NoReverseMatch:
        pass
    # User instance URLs
    try:
        user_instances = User.objects.all()
        if max_instances:
            user_instances = user_instances[:max_instances]
    except (AttributeError, User.DoesNotExist):
        user_instances = []
    for instance in user_instances:
        try:
            edit_url = reverse('wagtailusers_users:edit', args=[instance.pk])
            urls.append((user_model_name, "edit", f"{base_url}{edit_url}"))
        except NoReverseMatch:
            pass
        try:
            delete_url = reverse('wagtailusers_users:delete', args=[instance.pk])
            urls.append((user_model_name, "delete", f"{base_url}{delete_url}"))
        except NoReverseMatch:
            pass
    # Group URLs
    group_model_name = f"{Group._meta.app_label}.{Group.__name__}"
    try:
        group_add_url = reverse('wagtailusers_groups:add')
        urls.append((group_model_name, "add", f"{base_url}{group_add_url}"))
    except NoReverseMatch:
        pass
    try:
        group_index_url = reverse('wagtailusers_groups:index')
        urls.append((group_model_name, "index", f"{base_url}{group_index_url}"))
    except NoReverseMatch:
        pass
    try:
        group_instances = Group.objects.all()
        if max_instances:
            group_instances = group_instances[:max_instances]
    except (AttributeError, Group.DoesNotExist):
        group_instances = []
    for instance in group_instances:
        try:
            edit_url = reverse('wagtailusers_groups:edit', args=[instance.pk])
            urls.append((group_model_name, "edit", f"{base_url}{edit_url}"))
        except NoReverseMatch:
            pass
        try:
            delete_url = reverse('wagtailusers_groups:delete', args=[instance.pk])
            urls.append((group_model_name, "delete", f"{base_url}{delete_url}"))
        except NoReverseMatch:
            pass
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
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
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
