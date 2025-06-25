from collections import namedtuple
from io import StringIO

from django.conf import settings
from wagtail.admin.views.reports import ReportView
from wagtail.admin.widgets.button import HeaderButton

from .helpers.collection_helpers import get_collection_urls
from .helpers.document_helpers import get_document_urls
from .helpers.form_helpers import get_forms_urls
from .helpers.image_helpers import get_image_urls
from .helpers.locale_helpers import get_locale_urls
from .helpers.page_helpers import get_page_urls
from .helpers.redirect_helpers import get_redirects_urls
from .helpers.search_promotion_helpers import get_search_promotions_urls
from .helpers.settings_helpers import get_settings_urls
from .helpers.site_helpers import get_site_urls
from .helpers.snippet_helpers import get_snippet_urls
from .helpers.user_helpers import get_user_urls


class UnveilPageReportView(ReportView):
    index_url_name = "unveil_page_report"
    index_results_url_name = "unveil_page_report_results"
    header_icon = "tasks"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Page URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 1
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect page URLs
        page_urls = get_page_urls(output, base_url, max_instances)
        for model_name, url_type, url in page_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
        
        # # Get snippet models and collect snippet URLs
        # snippet_urls = get_snippet_urls(output, base_url, max_instances)
        # for model_name, url_type, url in snippet_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
        
        # # Create an empty dictionary for URL paths since we no longer get it from get_modelviewset_models()
        # modelviewset_urls = get_modelviewset_urls(output, base_url, max_instances)
        # for model_name, url_type, url in modelviewset_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
        
        # # Get modeladmin models and collect modeladmin URLs
        # modeladmin_urls = get_modeladmin_urls(output, base_url, max_instances)
        # for model_name, url_type, url in modeladmin_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
        
        # # Collect settings URLs
        # settings_urls = get_settings_admin_urls(output, base_url)
        # for model_name, url_type, url in settings_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
        
        # # Get image URLs
        # image_urls = get_image_admin_urls(output, base_url, max_instances)
        # for model_name, url_type, url in image_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
            
        # # Get document URLs
        # document_urls = get_document_admin_urls(output, base_url, max_instances)
        # for model_name, url_type, url in document_urls:
        #     all_urls.append(UrlEntry(counter, model_name, url_type, url))
        #     counter += 1
            
        return all_urls


class UnveilSnippetReportView(ReportView):
    index_url_name = "unveil_snippet_report"
    index_results_url_name = "unveil_snippet_report_results"
    header_icon = "tasks"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Snippet URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 1
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect snippet URLs
        snippet_urls = get_snippet_urls(output, base_url, max_instances)
        for model_name, url_type, url in snippet_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilImageReportView(ReportView):
    index_url_name = "unveil_image_report"
    index_results_url_name = "unveil_image_report_results"
    header_icon = "tasks"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Image URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 1
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect image URLs
        image_urls = get_image_urls(output, base_url, max_instances)
        for model_name, url_type, url in image_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilDocumentReportView(ReportView):
    index_url_name = "unveil_document_report"
    index_results_url_name = "unveil_document_report_results"
    header_icon = "tasks"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Document URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 1
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect document URLs
        document_urls = get_document_urls(output, base_url, max_instances)
        for model_name, url_type, url in document_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilSiteReportView(ReportView):
    index_url_name = "unveil_site_report"
    index_results_url_name = "unveil_site_report_results"
    header_icon = "tasks"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Site URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 10 (sites are typically few)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect site URLs
        site_urls = get_site_urls(output, base_url, max_instances)
        for model_name, url_type, url in site_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilUserReportView(ReportView):
    index_url_name = "unveil_user_report"
    index_results_url_name = "unveil_user_report_results"
    header_icon = "user"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil User URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 10 (users are typically more numerous)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect user URLs (users and groups)
        user_urls = get_user_urls(output, base_url, max_instances, self.request.user)
        for model_name, url_type, url in user_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilLocaleReportView(ReportView):
    index_url_name = "unveil_locale_report"
    index_results_url_name = "unveil_locale_report_results"
    header_icon = "globe"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Locale URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 20 (locales are typically few but may include many languages)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect locale URLs
        locale_urls = get_locale_urls(output, base_url, max_instances, self.request.user)
        for model_name, url_type, url in locale_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilFormReportView(ReportView):
    index_url_name = "unveil_form_report"
    index_results_url_name = "unveil_form_report_results"
    header_icon = "form"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Form URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 20 (forms can have many pages)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect form URLs
        form_urls = get_forms_urls(output, base_url, max_instances, self.request.user)
        for model_name, url_type, url in form_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilRedirectReportView(ReportView):
    index_url_name = "unveil_redirect_report"
    index_results_url_name = "unveil_redirect_report_results"
    header_icon = "redirect"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Redirect URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 20 (redirects can be numerous)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect redirect URLs
        redirect_urls = get_redirects_urls(output, base_url, max_instances, self.request.user)
        for model_name, url_type, url in redirect_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilSearchPromotionReportView(ReportView):
    index_url_name = "unveil_search_promotion_report"
    index_results_url_name = "unveil_search_promotion_report_results"
    header_icon = "search"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Search Promotion URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 20 (search promotions can be numerous)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect search promotion URLs
        search_promotion_urls = get_search_promotions_urls(output, base_url, max_instances, self.request.user)
        for model_name, url_type, url in search_promotion_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilSettingsReportView(ReportView):
    index_url_name = "unveil_settings_report"
    index_results_url_name = "unveil_settings_report_results"
    header_icon = "cog"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Settings URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 10 (settings models are typically few)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 10)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect settings URLs
        settings_urls = get_settings_urls(output, base_url, max_instances, self.request.user)
        for model_name, url_type, url in settings_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls


class UnveilCollectionReportView(ReportView):
    index_url_name = "unveil_collection_report"
    index_results_url_name = "unveil_collection_report_results"
    header_icon = "folder-open-1"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Collection URL's"
    list_export = [
        "id",
        "model_name",
        "url_type",
        "url",
    ]
    export_headings = {
        "id": "ID",
        "model_name": "Model Name",
        "url_type": "URL Type",
        "url": "URL",
    }
    paginate_by = None
    
    def get_header_buttons(self):
         return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={
                    "data-action": "check-urls",
                },
            ),
        ]

    def get_filterset_kwargs(self):
        # Get the base queryset and pass it to the filterset
        kwargs = super().get_filterset_kwargs()
        kwargs["queryset"] = self.get_queryset()
        return kwargs
    
    def get_base_queryset(self):
        # Return the base queryset for the report
        return self.get_queryset()

    def get_queryset(self):
        # Create a StringIO object to capture any output/errors
        output = StringIO()
        
        # Create a named tuple to represent URL entries
        UrlEntry = namedtuple('UrlEntry', ['id', 'model_name', 'url_type', 'url'])
        
        # Collect URLs from different helpers
        all_urls = []
        
        # We'll use a counter for IDs
        counter = 1
        
        # Get URLs from different sources using helper functions
        # Get max_instances from settings with a default of 20 (collections are typically moderate in number)
        max_instances = getattr(settings, 'WAGTAIL_UNVEIL_MAX_INSTANCES', 1)
        base_url = "http://localhost:8000"  # Default base URL
        
        # Collect collection URLs
        collection_urls = get_collection_urls(output, base_url, max_instances, self.request.user)
        for model_name, url_type, url in collection_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
            
        return all_urls