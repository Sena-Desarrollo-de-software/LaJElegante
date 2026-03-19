from django.test import TestCase
from django.urls import reverse


class CoreViewsTestCase(TestCase):

    def test_lobby_view_get(self):
        response = self.client.get(reverse("lobby"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/lobby.html")
        self.assertIn("carousel_items", response.context)
        self.assertIn("promos", response.context)
        self.assertEqual(len(response.context["carousel_items"]), 3)

    def test_tyc_view_get(self):
        response = self.client.get(reverse("tyc"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/tyc.html")
        self.assertIn("promos", response.context)

    def test_habitaciones_view_get(self):
        response = self.client.get(reverse("habitaciones"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/habitaciones.html")
        self.assertIn("special_room", response.context)
        self.assertIn("regular_rooms", response.context)
        self.assertIn("promo_data", response.context)
        self.assertIn("promos", response.context)
        self.assertEqual(len(response.context["regular_rooms"]), 3)

    def test_restaurante_view_get(self):
        response = self.client.get(reverse("restaurante"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/restaurante.html")
        self.assertIn("disponibilidad_data", response.context)
        self.assertIn("boton_data", response.context)
        self.assertIn("platos_list", response.context)
        self.assertIn("promos", response.context)
        self.assertEqual(len(response.context["platos_list"]), 2)

    def test_promociones_view_get(self):
        response = self.client.get(reverse("promociones"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/promociones.html")
        self.assertIn("promociones_nav", response.context)
        self.assertIn("promos", response.context)

    def test_signup_view_get(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/signup.html")
        self.assertIn("promos", response.context)

    def test_login_view_get(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "hotel/login.html")
        self.assertIn("promos", response.context)

    def test_lobby_view_post_not_allowed(self):
        response = self.client.post(reverse("lobby"))
        self.assertEqual(response.status_code, 405)

    def test_tyc_view_post_not_allowed(self):
        response = self.client.post(reverse("tyc"))
        self.assertEqual(response.status_code, 405)

    def test_habitaciones_view_post_not_allowed(self):
        response = self.client.post(reverse("habitaciones"))
        self.assertEqual(response.status_code, 405)

    def test_restaurante_view_post_not_allowed(self):
        response = self.client.post(reverse("restaurante"))
        self.assertEqual(response.status_code, 405)

    def test_promociones_view_post_not_allowed(self):
        response = self.client.post(reverse("promociones"))
        self.assertEqual(response.status_code, 405)

    def test_signup_view_post_not_allowed(self):
        response = self.client.post(reverse("signup"))
        self.assertEqual(response.status_code, 405)

    def test_login_view_post_not_allowed(self):
        response = self.client.post(reverse("login"))
        self.assertEqual(response.status_code, 405)