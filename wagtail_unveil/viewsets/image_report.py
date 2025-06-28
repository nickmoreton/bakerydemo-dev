from collections import namedtuple

from django.conf import settings
from django.urls import NoReverseMatch, path, reverse
from wagtail.admin.views.generic import IndexView
from wagtail.admin.viewsets.base import ViewSet
from wagtail.admin.widgets.button import HeaderButton
from wagtail.images import get_image_model


def get_image_index_url():
    # Get the index URL for images
    try:
        return reverse('wagtailimages:index')
    except NoReverseMatch:
        return None


def get_image_add_url():
    # Get the add URL for images
    try:
        return reverse('wagtailimages:add')
    except NoReverseMatch:
        return None


def get_image_edit_url(image_id):
    # Get the edit URL for an image
    try:
        return reverse('wagtailimages:edit', args=[image_id])
    except NoReverseMatch:
        return None


def get_image_delete_url(image_id):
    # Get the delete URL for an image
    try:
        return reverse('wagtailimages:delete', args=[image_id])
    except NoReverseMatch:
        return None


def get_image_urls(base_url, max_instances):
    # Return a list of tuples (model_name, url_type, url) for images
    urls = []
    index_url = get_image_index_url()
    if index_url:
        urls.append(('wagtail.Image', 'index', f"{base_url}{index_url}"))
    add_url = get_image_add_url()
    if add_url:
        urls.append(('wagtail.Image', 'add', f"{base_url}{add_url}"))
    Image = get_image_model()
    try:
        images = Image.objects.all()[:max_instances]
        for image in images:
            image_model_name = f"wagtail.Image_{image.id}_{getattr(image, 'title', getattr(image, 'name', ''))}"
            edit_url = get_image_edit_url(image.id)
            if edit_url:
                urls.append((image_model_name, 'edit', f"{base_url}{edit_url}"))
            delete_url = get_image_delete_url(image.id)
            if delete_url:
                urls.append((image_model_name, 'delete', f"{base_url}{delete_url}"))
    except Image.DoesNotExist:
        pass
    except (AttributeError, ValueError, TypeError):
        pass
    return urls


class UnveilImageReportIndexView(IndexView):
    # Index view for the Image Report
    template_name = "wagtail_unveil/unveil_url_report.html"
    results_template_name = "wagtail_unveil/unveil_url_report_results.html"
    page_title = "Unveil Image "
    header_icon = "image"
    paginate_by = None

    def get_queryset(self):
        # Get the queryset for image URLs
        UrlEntry = namedtuple("UrlEntry", ["id", "model_name", "url_type", "url"])
        all_urls = []
        counter = 1
        max_instances = getattr(settings, "WAGTAIL_UNVEIL_MAX_INSTANCES", 1)
        base_url = "http://localhost:8000"
        image_urls = get_image_urls(base_url, max_instances)
        for model_name, url_type, url in image_urls:
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
            )
        ]

    def get_context_data(self, **kwargs):
        # Get context data
        context = super().get_context_data(**kwargs)
        context["object_list"] = self.get_queryset()
        return context


class UnveilImageReportViewSet(ViewSet):
    # ViewSet for Unveil Image reports
    icon = "image"
    menu_label = "Image"
    menu_name = "unveil_image_report"
    url_namespace = "unveil_image_report"
    url_prefix = "unveil/image-report"
    index_view_class = UnveilImageReportIndexView

    def get_urlpatterns(self):
        # Return the URL patterns for this ViewSet
        return [
            path("", self.index_view_class.as_view(), name="index"),
            path("results/", self.index_view_class.as_view(), name="results"),
        ]


unveil_image_viewset = UnveilImageReportViewSet("unveil_image_report")
