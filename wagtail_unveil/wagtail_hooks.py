from django.urls import path, reverse

from wagtail.admin.menu import AdminOnlyMenuItem
from wagtail import hooks

from .views import UnveilReportView


@hooks.register("register_reports_menu_item")
def register_unveil_report_menu_item():
    """
    Register the Unveil report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil URL's",
        reverse("unveil_report"),
        name="unveil_report",
        order=10000,
        icon_name="tasks",
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    """
    Register the Unveil report view URL in the Wagtail admin.
    """
    return [
        path(
            "unveil/report/",
            UnveilReportView.as_view(),
            name="unveil_report",
        ),
        path(
            "unveil/report/results/",
            UnveilReportView.as_view(results_only=True),
            name="unveil_report_results",
        ),
    ]