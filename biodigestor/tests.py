from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from biodigestor.models import User, BioDigestor, Measurement
import json

class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password=make_password(salt='batatinha', password="password123")
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), "Test User")

    def test_check_password(self):
        self.assertTrue(self.user.check_password(make_password(salt='batatinha', password="password123")))
        self.assertFalse(self.user.check_password(make_password(salt='batatinha', password="wrongpassword")))

class BioDigestorModelTest(TestCase):

    def setUp(self):
        self.biodigestor = BioDigestor.objects.create(
            name="Test BioDigestor",
            description="This is a test biodigestor"
        )

    def test_biodigestor_str(self):
        self.assertEqual(str(self.biodigestor), "Test BioDigestor")

class MeasurementModelTest(TestCase):

    def setUp(self):
        self.measurement = Measurement.objects.create(
            internal_temperature=30.5,
            external_temperature=25.0,
            main_pressure=1.5,
            gas_level=0.75
        )

    def test_measurement_creation(self):
        self.assertEqual(self.measurement.internal_temperature, 30.5)
        self.assertEqual(self.measurement.external_temperature, 25.0)
        self.assertEqual(self.measurement.main_pressure, 1.5)
        self.assertEqual(self.measurement.gas_level, 0.75)

class UserViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "newpassword123"
        }

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello, world. You're at the biodigestor index.")

    def test_users_view_get(self):
        self.client.post(reverse('users'), data=json.dumps(self.user_data), content_type="application/json")
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.json())

    def test_users_view_post(self):
        response = self.client.post(reverse('users'), data=json.dumps(self.user_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["user"]["name"], "New User")

    def test_users_view_post_missing_field(self):
        response = self.client.post(reverse('users'), data=json.dumps({"name": "New User", "email": "", "password": "newpassword123"}), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_users_view_post_existing_user(self):
        User.objects.create(name="Existing User", email="newuser@example.com", password="password")
        response = self.client.post(reverse('users'), data=json.dumps(self.user_data), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_users_view_invalid_method(self):
        response = self.client.put(reverse('users'))
        self.assertEqual(response.status_code, 405)
        self.assertIn("error", response.json())

    def test_login_view_post(self):
        user = User.objects.create(
            name="Login User",
            email="loginuser@example.com",
            password=make_password(salt='batatinha', password="password123")
        )
        response = self.client.post(reverse('login'), data=json.dumps({"email": "loginuser@example.com", "password": "password123"}), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["user"]["name"], "Login User")

    def test_login_view_post_invalid_password(self):
        user = User.objects.create(
            name="Login User",
            email="loginuser@example.com",
            password=make_password(salt='batatinha', password="password123")
        )
        response = self.client.post(reverse('login'), data=json.dumps({"email": "loginuser@example.com", "password": "wrongpassword"}), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json())

    def test_login_view_post_invalid_method(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 405)
        self.assertIn("error", response.json())

    def test_login_view_post_user_not_found(self):
        response = self.client.post(reverse('login'), data=json.dumps({"email": "notfound@example.com", "password": "password123"}), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.json())


class BioDigestorViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.biodigestor_data = {
            "name": "New BioDigestor",
            "description": "Test BioDigestor description",
        }

    def test_create_biodigestor_view_post(self):
        response = self.client.post(reverse('biodigestors'), data=json.dumps(self.biodigestor_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["biodigestor"]["name"], "New BioDigestor")

    def test_list_biodigestor_view_get(self):
        self.client.post(reverse('biodigestors'), data=json.dumps(self.biodigestor_data), content_type="application/json")
        response = self.client.get(reverse('biodigestors'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("biodigestors", response.json())

    def test_biodigestor_view_invalid_method(self):
        response = self.client.put(reverse('biodigestors'))
        self.assertEqual(response.status_code, 405)
        self.assertIn("error", response.json())


class MeasurementViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.measurement_data = {
            "internal_temperature": 30.5,
            "external_temperature": 25.0,
            "main_pressure": 1.5,
            "gas_level": 0.75
        }

    def test_create_measurement_view_post(self):
        response = self.client.post(reverse('measurements'), data=json.dumps(self.measurement_data), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.json())
        self.assertEqual(response.json()["measurement"]["internal_temperature"], 30.5)

    def test_list_measurement_view_get(self):
        self.client.post(reverse('measurements'), data=json.dumps(self.measurement_data), content_type="application/json")
        response = self.client.get(reverse('measurements'))
        self.assertEqual(response.status_code, 200)
        self.assertIn("measurements", response.json())

    def test_measurement_view_invalid_method(self):
        response = self.client.put(reverse('measurements'))
        self.assertEqual(response.status_code, 405)
        self.assertIn("error", response.json())
