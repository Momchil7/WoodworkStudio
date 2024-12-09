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
    """
    View to list all projects (public).
    """
    model = Project
    template_name = 'projects/list-projects.html'
    context_object_name = 'projects'

class ProjectDetailView(DetailView):
    """
    View to display project details (public).
    """
    model = Project
    template_name = 'projects/details-project.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch a tutorial to pass to the context
        context['tutorial'] = Tutorial.objects.order_by('-created_at').first()  # Latest tutorial
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new project.
    """
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'
    success_url = reverse_lazy('core:dashboard')

    def form_valid(self, form):
        photo = form.save(commit=False)
        photo.user = self.request.user
        form.instance.created_by = self.request.user
        return super().form_valid(form)



class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/edit-project.html'

    def get_success_url(self):
        # Redirect to the edit page of the current project
        return reverse('content:project_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        # Set the created_by field to the current user
        form.instance.created_by = self.request.user

        # Optionally set other fields if needed
        photo = form.save(commit=False)
        photo.user = self.request.user

        return super().form_valid(form)




class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete a project.
    """
    model = Project
    template_name = 'projects/delete-project.html'
    success_url = reverse_lazy('core:dashboard')




class TutorialListView(ListView):
    """
    View to list all tutorials (public).
    """
    model = Tutorial
    template_name = 'tutorials/list-tutorials.html'
    context_object_name = 'tutorials'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add user favorites to the context
        # user_favorites = Favorite.objects.filter(user=self.request.user).values_list('tutorial_id', flat=True)
        if self.request.user.is_authenticated:
            # Add user favorites to the context if logged in
            user_favorites = Favorite.objects.filter(user=self.request.user).values_list('tutorial_id', flat=True)
        else:
            # Provide an empty list for unauthenticated users
            user_favorites = []
        context['user_favorites'] = user_favorites
        return context

class TutorialDetailView(DetailView):
    """
    View to display tutorial details (public).
    """
    model = Tutorial
    template_name = 'tutorials/details-tutorials.html'


class TutorialCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a new tutorial.
    """
    model = Tutorial
    form_class = TutorialForm
    template_name = 'tutorials/create-tutorials.html'
    success_url = reverse_lazy('core:dashboard')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TutorialUpdateView(LoginRequiredMixin, UpdateView):
    """
    View to edit an existing tutorial.
    """
    model = Tutorial
    form_class = TutorialForm
    template_name = 'tutorials/edit-tutorials.html'

    def get_success_url(self):
        # Redirect to the edit page of the current project
        return reverse('content:tutorial_detail', kwargs={'pk': self.object.pk})

class TutorialDeleteView(LoginRequiredMixin, DeleteView):
    """
    View to delete a tutorial.
    """
    model = Tutorial
    template_name = 'tutorials/delete-tutorials.html'
    success_url = reverse_lazy('core:dashboard')


@login_required
def add_favorite(request, tutorial_id):
    """
    Add a tutorial to favorites.
    """
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, tutorial=tutorial)
    return JsonResponse({'success': True, 'favorite_id': favorite.id})


@login_required
def remove_favorite(request, favorite_id):
    """
    Remove a tutorial from favorites.
    """
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    tutorial_id = favorite.tutorial.id  # Save tutorial ID before deleting
    favorite.delete()
    return JsonResponse({'success': True, 'tutorial_id': tutorial_id})


@login_required
def view_user_favorites(request, username):
    viewed_user = get_object_or_404(User, username=username)
    favorites = Favorite.objects.filter(user=viewed_user).select_related('tutorial')
    return render(request, 'tutorials/view-user-favorites.html', {
        'favorites': favorites,
        'viewed_user': viewed_user
    })

@login_required
def user_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('tutorial')
    return render(request, 'tutorials/user-favorites.html', {
        'favorites': favorites,
    })
