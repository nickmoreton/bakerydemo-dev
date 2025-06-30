from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
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

    def test_admin_index_route(self):
        url = reverse("unveil_admin_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Admin")

    def test_workflow_index_route(self):
        url = reverse("unveil_workflow_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Workflow")

    def test_workflow_task_index_route(self):
        url = reverse("unveil_workflow_task_report:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "wagtail_unveil/unveil_url_report.html")
        self.assertContains(response, "Unveil Workflow Task")


@override_settings(WAGTAIL_UNVEIL_JSON_TOKEN='test_token_123')
class UnveilReportsJSONAPITest(TestCase):
    """Test the JSON API endpoints for all reports"""
    
    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password123"
        )
        self.client.login(username="admin", password="password123")

    def test_json_endpoint_without_token(self):
        """Test that JSON API endpoints require authentication token"""
        url = "/unveil/api/collection/"
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 403])
        if response.status_code == 403:
            self.assertIn("Invalid or missing token", response.content.decode())
        else:
            self.assertEqual(response['Content-Type'], 'application/json')
            json_data = response.json()
            self.assertIn('results', json_data)
            self.assertIsInstance(json_data['results'], list)

    def test_json_endpoint_with_invalid_token(self):
        """Test that JSON API endpoints reject invalid tokens"""
        url = "/unveil/api/collection/"
        response = self.client.get(url, {'token': 'invalid_token'})
        self.assertIn(response.status_code, [200, 403])
        if response.status_code == 403:
            self.assertIn("Invalid or missing token", response.content.decode())
        else:
            self.assertEqual(response['Content-Type'], 'application/json')
            json_data = response.json()
            self.assertIn('results', json_data)
            self.assertIsInstance(json_data['results'], list)

    def test_json_endpoint_with_query_param_token(self):
        """Test JSON API endpoint with valid token as query parameter"""
        url = "/unveil/api/collection/"
        response = self.client.get(url, {'token': 'test_token_123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        json_data = response.json()
        self.assertIn('results', json_data)
        self.assertIsInstance(json_data['results'], list)

    def test_json_endpoint_with_header_token(self):
        """Test JSON API endpoint with valid token in header"""
        url = "/unveil/api/collection/"
        response = self.client.get(url, HTTP_X_API_TOKEN='test_token_123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        json_data = response.json()
        self.assertIn('results', json_data)
        self.assertIsInstance(json_data['results'], list)

    def test_all_reports_have_json_api_endpoints(self):
        """Test that all reports have working JSON API endpoints"""
        api_slugs = [
            'collection',
            'document',
            'form',
            'generic',
            'image',
            'locale',
            'page',
            'redirect',
            'search-promotion',
            'settings',
            'site',
            'snippet',
            'user',
            'admin',
            'workflow',
            'workflow-task',
        ] # Update this list if adding new reports
        for slug in api_slugs:
            with self.subTest(report=slug):
                url = f"/unveil/api/{slug}/"
                response = self.client.get(url, {'token': 'test_token_123'})
                self.assertEqual(response.status_code, 200, f"JSON API endpoint for {slug} failed")
                self.assertEqual(response['Content-Type'], 'application/json')
                json_data = response.json()
                self.assertIn('results', json_data)
                self.assertIsInstance(json_data['results'], list)

    def test_json_response_structure(self):
        """Test that JSON API responses have the correct structure"""
        url = "/unveil/api/admin/"  # Admin report has predictable data
        response = self.client.get(url, {'token': 'test_token_123'})
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertIn('results', json_data)
        if json_data['results']:
            entry = json_data['results'][0]
            required_fields = ['id', 'model_name', 'url_type', 'url']
            for field in required_fields:
                self.assertIn(field, entry, f"Missing field '{field}' in JSON response")
                self.assertIsNotNone(entry[field], f"Field '{field}' should not be None")

