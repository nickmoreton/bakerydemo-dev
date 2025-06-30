from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.viewsets.base import ViewSet
from wagtail.images import get_image_model

from wagtail_unveil.models import UrlEntry
from wagtail_unveil.viewsets.base import UnveilReportView, UnveilReportViewSet


def get_image_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, url) for images
    urls = []
    # Get the index URL for images
    try:
        index_url = reverse('wagtailimages:index')
        urls.append(('wagtail.Image', 'index', f"{base_url}{index_url}"))
    except NoReverseMatch:
        pass
    # Get the add URL for images
    try:
        add_url = reverse('wagtailimages:add')
        urls.append(('wagtail.Image', 'add', f"{base_url}{add_url}"))
    except NoReverseMatch:
        pass
    Image = get_image_model()
    try:
        images = Image.objects.all()[:max_instances]
        for image in images:
            image_model_name = f"wagtail.Image ({getattr(image, 'title', getattr(image, 'name', ''))})"
            # Get the edit URL for an image
            try:
                edit_url = reverse('wagtailimages:edit', args=[image.id])
                urls.append((image_model_name, 'edit', f"{base_url}{edit_url}"))
            except NoReverseMatch:
                pass
            # Get the delete URL for an image
            try:
                delete_url = reverse('wagtailimages:delete', args=[image.id])
                urls.append((image_model_name, 'delete', f"{base_url}{delete_url}"))
            except NoReverseMatch:
                pass
    except Image.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilImageReportIndexView(UnveilReportView):
    # Index view for the Image Report
    api_slug = "image"
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Image "
    header_icon = "image"
    paginate_by = None

    def get_queryset(self):
        # Get the queryset for image URLs
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = getattr(settings, "WAGTAIL_UNVEIL_BASE_URL", "http://localhost:8000")
        image_urls = get_image_urls(base_url, max_instances)
        for model_name, url_type, url in image_urls:
            all_urls.append(UrlEntry(counter, model_name, url_type, url))
            counter += 1
        return all_urls


class UnveilImageReportViewSet(UnveilReportViewSet):
    # ViewSet for Unveil Image reports
    icon = "image"
    menu_label = "Image"
    menu_name = "unveil_image_report"
    url_namespace = "unveil_image_report"
    url_prefix = "unveil/image-report"
    index_view_class = UnveilImageReportIndexView




unveil_image_viewset = UnveilImageReportViewSet("unveil_image_report")
