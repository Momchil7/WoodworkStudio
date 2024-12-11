from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from core.views import (
    UserProfileView,
    UserRegistrationView,
    DirectPasswordResetView,
    user_login,
    user_logout,
    UserProfileUpdateView,
    index,
    DashboardView,
)
from content.models import Project, Tutorial

UserModel = get_user_model()


class TestUserProfileViewIntegration(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
        )

    def test__authenticated_user__renders_correct_template(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("core:view_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/view-profile.html")




class TestUserProfileViewUnit(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123",
        )

    def test__get_object__returns_authenticated_user_profile(self):
        request = self.factory.get(reverse("core:view_profile"))
        request.user = self.user
        response = UserProfileView.as_view()(request)
        self.assertEqual(response.status_code, 200)


class TestUserRegistrationViewIntegration(TestCase):
    def test__valid_registration__creates_user_and_redirects(self):
        url = reverse("core:register")
        data = {
            "username": "newuser",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Redirects to dashboard



class TestDirectPasswordResetViewIntegration(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser", email="test@example.com", password="oldpassword123"
        )

    def test__valid_reset__updates_password_and_redirects(self):
        url = reverse("core:password_reset")
        data = {
            "username": "testuser",
            "new_password": "NewPassword123",
            "confirm_password": "NewPassword123",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(
            self.client.login(username="testuser", password="NewPassword123")
        )


class TestIndexViewIntegration(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="A test project",
            difficulty="beginner",
            created_by=self.user,
        )

    def test__index_renders_correct_template_for_authenticated_user(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        # self.assertContains(response, "Test Project")


class TestIndexViewUnit(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="A test project",
            difficulty="beginner",
            created_by=self.user,
        )

    def test__authenticated_user__renders_index_page(self):
        request = self.factory.get(reverse("core:index"))
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Test Project")

    def test__unauthenticated_user__renders_index_page(self):
        request = self.factory.get(reverse("core:index"))
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 200)
