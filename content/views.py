from django.shortcuts import render

# Create your views here.
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.models import User
from .models import Project
from .forms import ProjectForm
from .forms import TutorialForm
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favorite, Tutorial

class ProjectListView(ListView):
# публично вю за разглеждане на проекти
    model = Project
    template_name = 'projects/list-projects.html'
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    # публично вю за разглеждане на детайли на проекти
    model = Project
    template_name = 'projects/details-project.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) #добавяне на допълнителни данни в контекста
        # подаване на проект към контекста
        context['tutorial'] = Tutorial.objects.order_by('-created_at').first()  # Latest tutorial
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    # прайвът вю за създаване на проекти, позлва LoginRequiredMixin проверка на тип юзър и CreateView за създаване на нови записи.
    # проектът се създава и се свързва с потребителя, който го е създал.
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'
    success_url = reverse_lazy('core:dashboard')

    def form_valid(self, form):
        # опционално задаване на данни
        photo = form.save(commit=False)
        photo.user = self.request.user
        # сетване на created_by полето за текущ юзър
        form.instance.created_by = self.request.user
        # достъп до родителския клас, като преди това добавим наша логика,
        return super().form_valid(form)



class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/edit-project.html'

    def get_success_url(self):
        # редирект към страницата за едитване на проекта
        return reverse('content:project_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # сетване на created_by полето за текущ юзър
        form.instance.created_by = self.request.user
        # опжионално задаване на данни
        photo = form.save(commit=False)
        photo.user = self.request.user
        # достъп до родителския клас с наша логика,
        return super().form_valid(form)




class ProjectDeleteView(LoginRequiredMixin, DeleteView):
# изтриване на проект - не публично
    model = Project
    template_name = 'projects/delete-project.html'
    success_url = reverse_lazy('core:dashboard')




class TutorialListView(ListView):
# вю за преглеждане на туториали
    model = Tutorial
    template_name = 'tutorials/list-tutorials.html'
    context_object_name = 'tutorials'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # добавяме любими към контекста ако сме логнати
            user_favorites = Favorite.objects.filter(user=self.request.user).values_list('tutorial_id', flat=True)
        else:
            # добавяме празен лист към контекста ако НЕ сме логнати
            user_favorites = []
        context['user_favorites'] = user_favorites
        return context

class TutorialDetailView(DetailView):
# детайли за проекта - публично
    model = Tutorial
    template_name = 'tutorials/details-tutorials.html'


class TutorialCreateView(LoginRequiredMixin, CreateView):
# вю за създаване на проект - не публично
    model = Tutorial
    form_class = TutorialForm
    template_name = 'tutorials/create-tutorials.html'
    success_url = reverse_lazy('core:dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TutorialUpdateView(LoginRequiredMixin, UpdateView):
# вю за едитване на съществуващ проект
    model = Tutorial
    form_class = TutorialForm
    template_name = 'tutorials/edit-tutorials.html'

    def get_success_url(self):
        # редиректване към tutorial_detail на конкретния проект след едит
        return reverse('content:tutorial_detail', kwargs={'pk': self.object.pk})

class TutorialDeleteView(LoginRequiredMixin, DeleteView):

    model = Tutorial
    template_name = 'tutorials/delete-tutorials.html'
    success_url = reverse_lazy('core:dashboard')


@login_required
def add_favorite(request, tutorial_id):
    # взима tutorial от базата по  id ако няма такова връща 404
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    # търсим в базата за свързан любим туториал с потребител(created=False), ако няма такъв го създава
    favorite, created = Favorite.objects.get_or_create(user=request.user, tutorial=tutorial)
    # за JS скрипта - JSON отговор, който съдържа информация за успеха и ID-то на ново или съществуващо любимo
    return JsonResponse({'success': True, 'favorite_id': favorite.id})


@login_required
def remove_favorite(request, favorite_id):

    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    # запазване на туториала преди изтриване
    tutorial_id = favorite.tutorial.id
    favorite.delete()
    # за JS скрипта - JSON отговор, който съдържа информация за успеха и ID-то на tutorial-а, който е бил премахнат от любими
    return JsonResponse({'success': True, 'tutorial_id': tutorial_id})


@login_required
def view_user_favorites(request, username):
    viewed_user = get_object_or_404(User, username=username)
    # извлича всички записи от таблицата Favorite, които принадлежат на преглеждания потребител
    # select_related - ефективна SQL заявка, вместо да се правят отделни заявки за всеки tutorial
    favorites = Favorite.objects.filter(user=viewed_user).select_related('tutorial')
    #при рендериране на шаблона подаваме две променливи в контекста,
    return render(request, 'tutorials/view-user-favorites.html', {
        'favorites': favorites,
        'viewed_user': viewed_user
    })

@login_required
def user_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('tutorial')
    # подаваме променливата favorites, съдържаща  всички любими туториали на текущия потребител
    return render(request, 'tutorials/user-favorites.html', {
        'favorites': favorites,
    })
