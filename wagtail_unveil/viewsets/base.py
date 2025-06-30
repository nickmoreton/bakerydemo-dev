from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from django.urls import path
from wagtail.admin.views.reports import ReportView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton


class UnveilReportView(ReportView):
    """Base view class for Unveil reports"""
    
    def get_header_buttons(self):
        """Get header buttons for the report, using the explicit api_slug attribute."""
        api_slug = getattr(self, "api_slug", "collection")
        api_url = f"/unveil/api/{api_slug}/"
        return [
            HeaderButton(
                label="Json View",
                icon_name="code",
                url=api_url,
                attrs={"target": "_blank"},
            ),
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={"data-action": "check-urls"},
            ),
        ]


class UnveilReportViewSet(ViewSet):
    """Base ViewSet class for Unveil reports with JSON API support"""

    def as_json_view(self, request):
        """Return the report data as JSON with token authentication, unless user is superuser."""
        required_token = getattr(settings, 'WAGTAIL_UNVEIL_JSON_TOKEN', None)
        token = request.GET.get('token') or request.headers.get('X-API-TOKEN')
        # Bypass token check if user is authenticated and is superuser
        if not (hasattr(request, 'user') and request.user.is_authenticated and request.user.is_superuser):
            if not required_token or token != required_token:
                return HttpResponseForbidden("Invalid or missing token.")
        # Return the report data as JSON
        view = self.index_view_class()
        queryset = view.get_queryset()
        data = [
            {
                "id": entry.id,
                "model_name": entry.model_name,
                "url_type": entry.url_type,
                "url": entry.url,
            }
            for entry in queryset
        ]
        return JsonResponse({"results": data})

    def get_urlpatterns(self):
        """Return the URL patterns for this ViewSet including JSON endpoint"""
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]