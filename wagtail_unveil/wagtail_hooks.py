from django.urls import path, reverse
from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem

from .views import UnveilPageReportView, UnveilSnippetReportView, UnveilImageReportView, UnveilDocumentReportView, UnveilSiteReportView, UnveilUserReportView, UnveilLocaleReportView, UnveilFormReportView, UnveilRedirectReportView, UnveilSearchPromotionReportView


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


@hooks.register("register_reports_menu_item")
def register_unveil_document_report_menu_item():
    """
    Register the Unveil Document report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil Document URL's",
        reverse("unveil_document_report"),
        name="unveil_document_report",
        order=10003,
        icon_name="doc-full",
    )


@hooks.register("register_reports_menu_item")
def register_unveil_site_report_menu_item():
    """
    Register the Unveil Site report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil Site URL's",
        reverse("unveil_site_report"),
        name="unveil_site_report",
        order=10004,
        icon_name="site",
    )


@hooks.register("register_reports_menu_item")
def register_unveil_user_report_menu_item():
    """
    Register the Unveil User report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil User URL's",
        reverse("unveil_user_report"),
        name="unveil_user_report",
        order=10005,
        icon_name="user",
    )


@hooks.register("register_reports_menu_item")
def register_unveil_locale_report_menu_item():
    """
    Register the Unveil Locale report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil Locale URL's",
        reverse("unveil_locale_report"),
        name="unveil_locale_report",
        order=10006,
        icon_name="globe",
    )


@hooks.register("register_reports_menu_item")
def register_unveil_form_report_menu_item():
    """
    Register the Unveil Form report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil Form URL's",
        reverse("unveil_form_report"),
        name="unveil_form_report",
        order=10007,
        icon_name="form",
    )


@hooks.register("register_reports_menu_item")
def register_unveil_redirect_report_menu_item():
    """
    Register the Unveil Redirect report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil Redirect URL's",
        reverse("unveil_redirect_report"),
        name="unveil_redirect_report",
        order=10008,
        icon_name="redirect",
    )


@hooks.register("register_reports_menu_item")
def register_unveil_search_promotion_report_menu_item():
    """
    Register the Unveil Search Promotion report menu item in the Wagtail admin.
    """
    return AdminOnlyMenuItem(
        "Unveil Search Promotion URL's",
        reverse("unveil_search_promotion_report"),
        name="unveil_search_promotion_report",
        order=10009,
        icon_name="search",
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
        # Document Report URLs
        path(
            "unveil/document-report/",
            UnveilDocumentReportView.as_view(),
            name="unveil_document_report",
        ),
        path(
            "unveil/document-report/results/",
            UnveilDocumentReportView.as_view(results_only=True),
            name="unveil_document_report_results",
        ),
        # Site Report URLs
        path(
            "unveil/site-report/",
            UnveilSiteReportView.as_view(),
            name="unveil_site_report",
        ),
        path(
            "unveil/site-report/results/",
            UnveilSiteReportView.as_view(results_only=True),
            name="unveil_site_report_results",
        ),
        # User Report URLs
        path(
            "unveil/user-report/",
            UnveilUserReportView.as_view(),
            name="unveil_user_report",
        ),
        path(
            "unveil/user-report/results/",
            UnveilUserReportView.as_view(results_only=True),
            name="unveil_user_report_results",
        ),
        # Locale Report URLs
        path(
            "unveil/locale-report/",
            UnveilLocaleReportView.as_view(),
            name="unveil_locale_report",
        ),
        path(
            "unveil/locale-report/results/",
            UnveilLocaleReportView.as_view(results_only=True),
            name="unveil_locale_report_results",
        ),
        # Form Report URLs
        path(
            "unveil/form-report/",
            UnveilFormReportView.as_view(),
            name="unveil_form_report",
        ),
        path(
            "unveil/form-report/results/",
            UnveilFormReportView.as_view(results_only=True),
            name="unveil_form_report_results",
        ),
        # Redirect Report URLs
        path(
            "unveil/redirect-report/",
            UnveilRedirectReportView.as_view(),
            name="unveil_redirect_report",
        ),
        path(
            "unveil/redirect-report/results/",
            UnveilRedirectReportView.as_view(results_only=True),
            name="unveil_redirect_report_results",
        ),
        # Search Promotion Report URLs
        path(
            "unveil/search-promotion-report/",
            UnveilSearchPromotionReportView.as_view(),
            name="unveil_search_promotion_report",
        ),
        path(
            "unveil/search-promotion-report/results/",
            UnveilSearchPromotionReportView.as_view(results_only=True),
            name="unveil_search_promotion_report_results",
        ),
    ]