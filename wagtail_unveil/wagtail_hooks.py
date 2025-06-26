from wagtail import hooks
from wagtail.admin.viewsets.base import ViewSetGroup

# Import ViewSet Group
from .viewsets.collection_report import unveil_collection_viewset
from .viewsets.document_report import unveil_document_viewset
from .viewsets.page_report import UnveilPageReportViewSet
from .viewsets.image_report import UnveilImageReportViewSet
from .viewsets.search_promotion_report import UnveilSearchPromotionReportViewSet
from .viewsets.redirect_report import UnveilRedirectReportViewSet
from .viewsets.site_report import UnveilSiteReportViewSet
from .viewsets.form_report import UnveilFormReportViewSet
from .viewsets.locale_report import UnveilLocaleReportViewSet
from .viewsets.snippet_report import UnveilSnippetReportViewSet
from .viewsets.user_report import UnveilUserReportViewSet
from .viewsets.generic_report import UnveilGenericReportViewSet
from .viewsets.settings_report import UnveilSettingsReportViewSet

# Instantiate all ViewSets
unveil_page_viewset = UnveilPageReportViewSet()
unveil_image_viewset = UnveilImageReportViewSet()
unveil_search_promotion_viewset = UnveilSearchPromotionReportViewSet()
unveil_redirect_viewset = UnveilRedirectReportViewSet()
unveil_site_viewset = UnveilSiteReportViewSet()
unveil_form_viewset = UnveilFormReportViewSet()
unveil_locale_viewset = UnveilLocaleReportViewSet()
unveil_snippet_viewset = UnveilSnippetReportViewSet()
unveil_user_viewset = UnveilUserReportViewSet()
unveil_generic_viewset = UnveilGenericReportViewSet()
unveil_settings_viewset = UnveilSettingsReportViewSet()


class UnveilReportsViewSetGroup(ViewSetGroup):
    """
    ViewSet group for all Unveil reports.

    This groups all Unveil report ViewSets under a single "Unveil" menu item
    in the Wagtail admin interface.
    """

    menu_label = "Unveil Reports"
    menu_icon = "tasks"
    menu_order = 400  # Position in the menu
    items = (
        unveil_collection_viewset,
        unveil_document_viewset,
        unveil_page_viewset,
        unveil_image_viewset,
        unveil_search_promotion_viewset,
        unveil_redirect_viewset,
        unveil_site_viewset,
        unveil_form_viewset,
        unveil_locale_viewset,
        unveil_snippet_viewset,
        unveil_user_viewset,
        unveil_generic_viewset,
        unveil_settings_viewset,
    )


# Register the ViewSet Group for Unveil Reports
@hooks.register("register_admin_viewset")
def register_unveil_reports_viewset_group():
    """
    Register the Unveil Reports ViewSet Group with Wagtail admin.
    This creates a grouped menu structure for all Unveil reports.
    """
    return UnveilReportsViewSetGroup()


# Remove or comment out all @hooks.register("register_reports_menu_item") functions for migrated reports


# All old menu item registrations for migrated reports are now removed/commented out.


@hooks.register("register_admin_urls")
def register_admin_urls():
    """
    Register the Unveil report view URLs in the Wagtail admin.
    """
    return [
        # Only keep non-migrated report URLs here (if any). All migrated reports are now handled by ViewSets.
        # If all reports are migrated, this list can be empty or removed entirely.
    ]
