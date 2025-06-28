from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.contrib.search_promotions.models import SearchPromotion


def get_search_promotion_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, url) for search promotions
    urls = []
    # Get the index URL for search promotions
    try:
        index_url = reverse('wagtailsearchpromotions:index')
        urls.append(('wagtail.SearchPromotion', 'index', f"{base_url}{index_url}"))
    except NoReverseMatch:
        pass
    # Get the add URL for search promotions
    try:
        add_url = reverse('wagtailsearchpromotions:add')
        urls.append(('wagtail.SearchPromotion', 'add', f"{base_url}{add_url}"))
    except NoReverseMatch:
        pass
    try:
        promotions = SearchPromotion.objects.all()[:max_instances]
        for promotion in promotions:
            promotion_model_name = f"wagtail.SearchPromotion_{promotion.id}_{getattr(promotion, 'query', '')}"
            # Get the edit URL for a search promotion
            try:
                edit_url = reverse('wagtailsearchpromotions:edit', args=[promotion.id])
                urls.append((promotion_model_name, 'edit', f"{base_url}{edit_url}"))
            except NoReverseMatch:
                pass
            # Get the delete URL for a search promotion
            try:
                delete_url = reverse('wagtailsearchpromotions:delete', args=[promotion.id])
                urls.append((promotion_model_name, 'delete', f"{base_url}{delete_url}"))
            except NoReverseMatch:
                pass
    except SearchPromotion.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilSearchPromotionReportIndexView(IndexView):
    # Index view for the Search Promotion Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Search Promotion"
    header_icon = "pick"
    paginate_by = None

    def get_queryset(self):
        # Get the queryset for search promotion URLs
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        promo_urls = get_search_promotion_urls(base_url, max_instances)
        for model_name, url_type, url in promo_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
        return all_urls

    def get_header_buttons(self):
        # Get header buttons
        return [
            HeaderButton(
                label="Run Checks",
                icon_name="link",
                attrs={"data-action": "check-urls"},
            ),
        ]


class UnveilSearchPromotionReportViewSet(ViewSet):
    # ViewSet for Unveil Search Promotion reports
    icon = "pick"
    menu_label = "Search Promotion"
    menu_name = "unveil_search_promotion_report"
    url_namespace = "unveil_search_promotion_report"
    url_prefix = "unveil/search-promotion-report"
    index_view_class = UnveilSearchPromotionReportIndexView

    def get_urlpatterns(self):
        # Return the URL patterns for this ViewSet
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


# Create an instance of the ViewSet to be registered
unveil_search_promotion_viewset = UnveilSearchPromotionReportViewSet()
