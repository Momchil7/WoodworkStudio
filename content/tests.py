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
        # инициализиране на  RequestFactory() за симулирани заявки
        self.factory = RequestFactory()

        # създаваме потребител
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

        # създаване на проект с свързан юзър
        self.project = Project.objects.create(
            title="Test Project",
            description="Test Description",
            difficulty="beginner",
            created_by=self.user
        )

    def test__project_detail_view__renders_correct_template(self):
        # създаване на рекуеста
        request = self.factory.get(reverse('content:project_detail', kwargs={'pk': self.project.pk}))
        request.user = self.user  # Assign an authenticated user

        # извикване на вюто с аргумент
        response = ProjectDetailView.as_view()(request, pk=self.project.pk)

        # проверка на статуса
        self.assertEqual(response.status_code, 200)

        # проверка на заявка, дали е генериран отговор с шаблона projects/details-project.html
        self.assertIn('projects/details-project.html', response.template_name)





class TestTutorialListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test__tutorial_list_view__renders_correct_template(self):
        # създаване на заявка с анонимен потребител
        request = self.factory.get(reverse('content:tutorial_list'))
        request.user = AnonymousUser()  # Or use a real user if needed

        # извикване на вюто с рекуеста
        response = TutorialListView.as_view()(request)

        # проверка на код
        self.assertEqual(response.status_code, 200)

        # проверка за правилен шаблон
        self.assertIn('tutorials/list-tutorials.html', response.template_name)



class TestTutorialDetailView(TestCase):
    def setUp(self):

        self.factory = RequestFactory()

        # създаване на потребител
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )

        # създаване на туториал с асоцийран потребител
        self.tutorial = Tutorial.objects.create(
            title="Test tutorial",
            content="Test content",
            skill_level="beginner",
            created_by=self.user
        )

    def test__tutorial_detail_view__renders_correct_template(self):
        # GET заявка към URL-а, който води към tutorial_detail с пк на туториала
        request = self.factory.get(reverse('content:tutorial_detail', kwargs={'pk': self.tutorial.pk}))
        request.user = self.user  # Assign an authenticated user

        #  извикване на вю с рикуеста и пк
        response = TutorialDetailView.as_view()(request, pk=self.tutorial.pk)

        # проверка на статуса
        self.assertEqual(response.status_code, 200)

        # проверка за правилен шаблон
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

    # тестване добавяне на "favorite" и правилен запис в базата данни.
    def test__add_favorite__creates_favorite(self):
        response = self.client.post(reverse('content:add_favorite', kwargs={'tutorial_id': self.tutorial.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(user=self.user, tutorial=self.tutorial).exists())

    def test__remove_favorite__deletes_favorite(self):
        favorite = Favorite.objects.create(user=self.user, tutorial=self.tutorial) #запис в базата данни за "favorite", който свързва потребителя и tutorial
        response = self.client.post(reverse('content:remove_favorite', kwargs={'favorite_id': favorite.id}))#POST заявка за премахване на любим tutorial
        self.assertEqual(response.status_code, 200)#
        self.assertFalse(Favorite.objects.filter(id=favorite.id).exists())#


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
