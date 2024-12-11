from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse
from content.models import Project
from content.views import ProjectListView, ProjectDetailView, TutorialListView, TutorialDetailView
from django.contrib.auth import get_user_model
from content.models import Tutorial, Favorite
from core.models import User

UserModel = get_user_model()

class TestProjectListView(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

        # Create a project associated with the user
        self.project = Project.objects.create(
            title="Test Project",
            description="Test Description",
            difficulty="beginner",
            created_by=self.user
        )

    def test__project_list_view__renders_correct_template(self):
        response = self.client.get(reverse('content:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/list-projects.html')



class TestProjectDetailView(TestCase):
    def setUp(self):
        # Initialize RequestFactory
        self.factory = RequestFactory()

        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

        # Create a project associated with the user
        self.project = Project.objects.create(
            title="Test Project",
            description="Test Description",
            difficulty="beginner",
            created_by=self.user
        )

    def test__project_detail_view__renders_correct_template(self):
        # Generate the request using the factory
        request = self.factory.get(reverse('content:project_detail', kwargs={'pk': self.project.pk}))
        request.user = self.user  # Assign an authenticated user

        # Call the view directly with the request and kwargs
        response = ProjectDetailView.as_view()(request, pk=self.project.pk)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Verify the template used (directly check `response.template_name`)
        self.assertIn('projects/details-project.html', response.template_name)





class TestTutorialListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test__tutorial_list_view__renders_correct_template(self):
        # Create a request and manually set the user (AnonymousUser for unauthenticated tests)
        request = self.factory.get(reverse('content:tutorial_list'))
        request.user = AnonymousUser()  # Or use a real user if needed

        # Call the view with the request
        response = TutorialListView.as_view()(request)

        # Verify response status code
        self.assertEqual(response.status_code, 200)

        # Check if the correct template is used
        self.assertIn('tutorials/list-tutorials.html', response.template_name)



class TestTutorialDetailView(TestCase):
    def setUp(self):
        # Initialize RequestFactory
        self.factory = RequestFactory()

        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

        # Create a project associated with the user
        self.tutorial = Tutorial.objects.create(
            title="Test tutorial",
            content="Test content",
            skill_level="beginner",
            created_by=self.user
        )

    def test__tutorial_detail_view__renders_correct_template(self):
        # request = self.factory.get(reverse('content:tutorial_detail', kwargs={'pk': self.tutorial.pk}))
        # response = TutorialDetailView.as_view()(request, pk=self.tutorial.pk)
        # self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'tutorials/details-tutorials.html')
        request = self.factory.get(reverse('content:tutorial_detail', kwargs={'pk': self.tutorial.pk}))
        request.user = self.user  # Assign an authenticated user

        # Call the view directly with the request and kwargs
        response = TutorialDetailView.as_view()(request, pk=self.tutorial.pk)

        # Check the response status code
        self.assertEqual(response.status_code, 200)

        # Verify the template used (directly check `response.template_name`)
        self.assertIn('tutorials/details-tutorials.html', response.template_name)




class TestFavoriteViews(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username="testuser", password="password123")
        self.tutorial = Tutorial.objects.create(
            title="Test tutorial",
            content="Test content",
            skill_level="beginner",
            created_by=self.user
        )
        self.client.login(username="testuser", password="password123")

    def test__add_favorite__creates_favorite(self):
        response = self.client.post(reverse('content:add_favorite', kwargs={'tutorial_id': self.tutorial.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(user=self.user, tutorial=self.tutorial).exists())

    def test__remove_favorite__deletes_favorite(self):
        favorite = Favorite.objects.create(user=self.user, tutorial=self.tutorial)
        response = self.client.post(reverse('content:remove_favorite', kwargs={'favorite_id': favorite.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorite.objects.filter(id=favorite.id).exists())


class TestViewUserFavorites(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.tutorial = Tutorial.objects.create(title="Test Tutorial", content="Tutorial content")
        self.favorite = Favorite.objects.create(user=self.user, tutorial=self.tutorial)

    def test__view_user_favorites__renders_correct_template(self):
        response = self.client.get(reverse('content:view_user_favorites', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutorials/view-user-favorites.html')
        self.assertContains(response, self.tutorial.title)
