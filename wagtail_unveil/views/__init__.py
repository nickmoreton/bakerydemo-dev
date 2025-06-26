# Import all ReportView classes for backwards compatibility
from .page_report import UnveilPageReportView
from .snippet_report import UnveilSnippetReportView
from .image_report import UnveilImageReportView
from .document_report import UnveilDocumentReportView
from .site_report import UnveilSiteReportView
from .user_report import UnveilUserReportView
from .locale_report import UnveilLocaleReportView
from .form_report import UnveilFormReportView
from .redirect_report import UnveilRedirectReportView
from .search_promotion_report import UnveilSearchPromotionReportView
from .settings_report import UnveilSettingsReportView
from .collection_report import UnveilCollectionReportView
from .generic_report import UnveilGenericReportView

__all__ = [
    'UnveilPageReportView',
    'UnveilSnippetReportView',
    'UnveilImageReportView',
    'UnveilDocumentReportView',
    'UnveilSiteReportView',
    'UnveilUserReportView',
    'UnveilLocaleReportView',
    'UnveilFormReportView',
    'UnveilRedirectReportView',
    'UnveilSearchPromotionReportView',
    'UnveilSettingsReportView',
    'UnveilCollectionReportView',
    'UnveilGenericReportView',
]
