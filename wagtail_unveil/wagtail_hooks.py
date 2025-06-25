from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem

from .views import UnveilPageReportView, UnveilSnippetReportView, UnveilImageReportView


@hooks.register("register_reports_menu_item")
def register_unveil_page_report_menu_item():
    """
    Register the Unveil Page report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil Page URL's",
        reverse("unveil_page_report"),
        name="unveil_page_report",
        order=10000,
        icon_name="tasks",
    )


@hooks.register("register_reports_menu_item")
def register_unveil_snippet_report_menu_item():
    """
    Register the Unveil Snippet report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil Snippet URL's",
        reverse("unveil_snippet_report"),
        name="unveil_snippet_report",
        order=10001,
        icon_name="snippet",
    )


@hooks.register("register_reports_menu_item")
def register_unveil_image_report_menu_item():
    """
    Register the Unveil Image report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil Image URL's",
        reverse("unveil_image_report"),
        name="unveil_image_report",
        order=10002,
        icon_name="image",
    )


@hooks.register("register_admin_urls")
def register_admin_urls():
    """
    Register the Unveil report view URLs in the Wagtail admin.
    """
    return [
        # Page Report URLs
        path(
            "unveil/page-report/",
            UnveilPageReportView.as_view(),
            name="unveil_page_report",
        ),
        path(
            "unveil/page-report/results/",
            UnveilPageReportView.as_view(results_only=True),
            name="unveil_page_report_results",
        ),
        # Snippet Report URLs
        path(
            "unveil/snippet-report/",
            UnveilSnippetReportView.as_view(),
            name="unveil_snippet_report",
        ),
        path(
            "unveil/snippet-report/results/",
            UnveilSnippetReportView.as_view(results_only=True),
            name="unveil_snippet_report_results",
        ),
        # Image Report URLs
        path(
            "unveil/image-report/",
            UnveilImageReportView.as_view(),
            name="unveil_image_report",
        ),
        path(
            "unveil/image-report/results/",
            UnveilImageReportView.as_view(results_only=True),
            name="unveil_image_report_results",
        ),
        # Image Report URLs
        path(
            "unveil/image-report/",
            UnveilImageReportView.as_view(),
            name="unveil_image_report",
        ),
        path(
            "unveil/image-report/results/",
            UnveilImageReportView.as_view(results_only=True),
            name="unveil_image_report_results",
        ),
    ]