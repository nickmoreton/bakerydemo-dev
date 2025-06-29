from wagtail.admin.views.reports import ReportView
from wagtail.admin.widgets.button import HeaderButton


class UnveilReportView(ReportView):
    def get_header_buttons(self):
        # Get header buttons
        return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]