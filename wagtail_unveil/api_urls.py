from django.urls import path

from wagtail_unveil.viewsets.admin_report import UnveilAdminReportViewSet
from wagtail_unveil.viewsets.collection_report import UnveilCollectionReportViewSet
from wagtail_unveil.viewsets.document_report import UnveilDocumentReportViewSet
from wagtail_unveil.viewsets.form_report import UnveilFormReportViewSet
from wagtail_unveil.viewsets.generic_report import UnveilGenericReportViewSet
from wagtail_unveil.viewsets.image_report import UnveilImageReportViewSet
from wagtail_unveil.viewsets.locale_report import UnveilLocaleReportViewSet
from wagtail_unveil.viewsets.page_report import UnveilPageReportViewSet
from wagtail_unveil.viewsets.redirect_report import UnveilRedirectReportViewSet
from wagtail_unveil.viewsets.search_promotion_report import (
    UnveilSearchPromotionReportViewSet,
)
from wagtail_unveil.viewsets.settings_report import UnveilSettingsReportViewSet
from wagtail_unveil.viewsets.site_report import UnveilSiteReportViewSet
from wagtail_unveil.viewsets.snippet_report import UnveilSnippetReportViewSet
from wagtail_unveil.viewsets.user_report import UnveilUserReportViewSet
from wagtail_unveil.viewsets.workflow_report import UnveilWorkflowReportViewSet
from wagtail_unveil.viewsets.workflow_task_report import UnveilWorkflowTaskReportViewSet

# You can import and add other report viewsets here as needed

collection_api_viewset = UnveilCollectionReportViewSet()
document_api_viewset = UnveilDocumentReportViewSet()
form_api_viewset = UnveilFormReportViewSet()
generic_api_viewset = UnveilGenericReportViewSet()
image_api_viewset = UnveilImageReportViewSet()
locale_api_viewset = UnveilLocaleReportViewSet()
page_api_viewset = UnveilPageReportViewSet()
redirect_api_viewset = UnveilRedirectReportViewSet()
search_promotion_api_viewset = UnveilSearchPromotionReportViewSet()
settings_api_viewset = UnveilSettingsReportViewSet()
site_api_viewset = UnveilSiteReportViewSet()
snippet_api_viewset = UnveilSnippetReportViewSet()
user_api_viewset = UnveilUserReportViewSet()
admin_api_viewset = UnveilAdminReportViewSet()
workflow_api_viewset = UnveilWorkflowReportViewSet()
workflow_task_api_viewset = UnveilWorkflowTaskReportViewSet()

urlpatterns = [
    path('collection/', collection_api_viewset.as_json_view),
    path('document/', document_api_viewset.as_json_view),
    path('form/', form_api_viewset.as_json_view),
    path('generic/', generic_api_viewset.as_json_view),
    path('image/', image_api_viewset.as_json_view),
    path('locale/', locale_api_viewset.as_json_view),
    path('page/', page_api_viewset.as_json_view),
    path('redirect/', redirect_api_viewset.as_json_view),
    path('search-promotion/', search_promotion_api_viewset.as_json_view),
    path('settings/', settings_api_viewset.as_json_view),
    path('site/', site_api_viewset.as_json_view),
    path('snippet/', snippet_api_viewset.as_json_view),
    path('user/', user_api_viewset.as_json_view),
    path('admin/', admin_api_viewset.as_json_view),
    path('workflow/', workflow_api_viewset.as_json_view),
    path('workflow-task/', workflow_task_api_viewset.as_json_view),
]
