from wagtail import hooks
from wagtail.admin.viewsets.base import ViewSetGroup

from .viewsets.admin_report import unveil_admin_viewset
from .viewsets.collection_report import unveil_collection_viewset
from .viewsets.document_report import unveil_document_viewset
from .viewsets.form_report import unveil_form_viewset
from .viewsets.generic_report import unveil_generic_viewset
from .viewsets.image_report import unveil_image_viewset
from .viewsets.locale_report import unveil_locale_viewset
from .viewsets.page_report import unveil_page_viewset
from .viewsets.redirect_report import unveil_redirect_viewset
from .viewsets.search_promotion_report import unveil_search_promotion_viewset
from .viewsets.settings_report import unveil_settings_viewset
from .viewsets.site_report import unveil_site_viewset
from .viewsets.snippet_report import unveil_snippet_viewset
from .viewsets.user_report import unveil_user_viewset
from .viewsets.workflow_report import unveil_workflow_viewset
from .viewsets.workflow_task_report import unveil_workflow_task_viewset


class UnveilReportsViewSetGroup(ViewSetGroup):
    """
    ViewSet group for all Unveil reports.

    This groups all Unveil report ViewSets under a single "Unveil" menu item
    in the Wagtail admin interface.
    """

    menu_label = "Unveil Reports"
    menu_icon = "tasks"
    menu_order = 1  # Position in the menu
    items = (
        unveil_page_viewset,
        unveil_image_viewset,
        unveil_document_viewset,
        unveil_form_viewset,
        unveil_snippet_viewset,
        unveil_generic_viewset,
        unveil_search_promotion_viewset,
        unveil_collection_viewset,
        unveil_redirect_viewset,
        unveil_settings_viewset,
        unveil_user_viewset,
        unveil_site_viewset,
        unveil_locale_viewset,
        unveil_admin_viewset,
        unveil_workflow_viewset,
        unveil_workflow_task_viewset,
    )


# ViewSet Group for Unveil Reports
@hooks.register("register_admin_viewset")
def register_unveil_reports_viewset_group():
    """
    Register the Unveil Reports ViewSet Group with Wagtail admin.
    This creates a grouped menu structure for all Unveil reports.
    """
    return UnveilReportsViewSetGroup()
