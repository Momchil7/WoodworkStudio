from django.urls import path
from .views import (
    ProjectListView, ProjectDetailView, ProjectUpdateView, ProjectDeleteView,
    TutorialListView, TutorialDetailView, TutorialCreateView, TutorialUpdateView, TutorialDeleteView,
    add_favorite, remove_favorite, ProjectCreateView, user_favorites, view_user_favorites,
    # create_project,

)

app_name = 'content'

urlpatterns = [
    # Project Views
    path('projects/', ProjectListView.as_view(), name='project_list'),  # List of projects
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),  # Project details
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),  # Create a project
    path('projects/<int:pk>/edit/', ProjectUpdateView.as_view(), name='project_edit'),  # Edit a project
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),  # Delete a project



    # Tutorial Views
    path('tutorials/', TutorialListView.as_view(), name='tutorial_list'),  # List of tutorials
    path('tutorials/<int:pk>/', TutorialDetailView.as_view(), name='tutorial_detail'),  # Tutorial details
    path('tutorials/create/', TutorialCreateView.as_view(), name='tutorial_create'),  # Create a tutorial
    path('tutorials/<int:pk>/edit/', TutorialUpdateView.as_view(), name='tutorial_edit'),  # Edit a tutorial
    path('tutorials/<int:pk>/delete/', TutorialDeleteView.as_view(), name='tutorial_delete'),  # Delete a tutorial

    # Favorites Views
    path('favorites/', user_favorites, name='user_favorites'),
    path('favorites/add/<int:tutorial_id>/', add_favorite, name='add_favorite'),  # Add a tutorial to favorites
    path('favorites/remove/<int:favorite_id>/', remove_favorite, name='remove_favorite'),  # Remove a tutorial from favorites

    # path('profile/<str:username>/favorites/', view_user_favorites, name='view_user_favorites'),
]
