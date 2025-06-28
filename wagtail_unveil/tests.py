from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UnveilReportsIndexViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password123"
        )
        self.client.login(username="admin", password="password123")

    def test_collection_index_route(self):
        url = reverse("unveil_collection_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Collection")

    def test_document_index_route(self):
        url = reverse("unveil_document_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Document")

    def test_form_index_route(self):
        url = reverse("unveil_form_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Form")

    def test_generic_index_route(self):
        url = reverse("unveil_generic_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Generic")

    def test_image_index_route(self):
        url = reverse("unveil_image_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Image")

    def test_locale_index_route(self):
        url = reverse("unveil_locale_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Locale")

    def test_page_index_route(self):
        url = reverse("unveil_page_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Page")

    def test_redirect_index_route(self):
        url = reverse("unveil_redirect_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Redirect")

    def test_search_promotion_index_route(self):
        url = reverse("unveil_search_promotion_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Search Promotion")

    def test_settings_index_route(self):
        url = reverse("unveil_settings_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Settings")

    def test_site_index_route(self):
        url = reverse("unveil_site_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Site")

    def test_snippet_index_route(self):
        url = reverse("unveil_snippet_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Snippet")

    def test_user_index_route(self):
        url = reverse("unveil_user_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil User")

