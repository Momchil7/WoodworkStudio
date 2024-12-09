from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib import messages
from content.models import Project, Tutorial
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import UserProfileForm
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

# from .forms import SearchForm

from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404


class UserProfileView(DetailView):
    """
    View for displaying a user's profile.
    """
    model = User
    template_name = 'registration/view-profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        # Retrieve the user based on a URL parameter (e.g., `username`) or default to the current user
        username = self.kwargs.get('username')
        if username:
            return get_object_or_404(User, username=username)
        return self.request.user


class UserRegistrationView(CreateView):
    """
    View for user registration.
    """
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('core:dashboard')  # Redirect after successful registration

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Automatically log in the user
        return response


class DirectPasswordResetView(View):
    template_name = 'registration/password_reset.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not new_password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, self.template_name)

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, self.template_name)

        try:
            user = User.objects.get(username=username)
            user.password = make_password(new_password)  # Hash and save the new password
            user.save()
            messages.success(request, "Password reset successfully. You can now log in.")
            return redirect(reverse_lazy('core:login'))
        except User.DoesNotExist:
            messages.error(request, "User with this username does not exist.")
            return render(request, self.template_name)




def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # Log in the user
            from django.contrib.auth import login
            login(request, form.get_user())
            return redirect('core:dashboard')  # Redirect after successful login
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {'form': form})




@login_required
def user_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html', {})



class UserProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    View for updating user profile.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'registration/update-profile.html'
    # success_url = reverse_lazy('core:dashboard')  # Redirect after update
    success_message = "Your profile was updated successfully!"

    def get_success_url(self):
        # Redirect to the edit page of the current project
        return reverse('core:view_profile')

    def get_object(self, queryset=None):
        return self.request.user  # Ensure users can only edit their own profile



def index(request):
    """
    Public landing page.
    """
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'index.html', context)




class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Private dashboard for authenticated users.
    """
    template_name = 'dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.request.user  # Pass the user object as 'profile'
        context['projects'] = Project.objects.filter(created_by=self.request.user).order_by('-created_at')
        context['tutorials'] = Tutorial.objects.filter(created_by=self.request.user).order_by('-created_at')
        return context





