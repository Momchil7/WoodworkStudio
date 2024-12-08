from django.contrib import admin

# Register your models here.
from django.contrib import admin

from content.models import Project, Tutorial, Category, Favorite


# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'difficulty', 'status', 'created_at')  # Show key project info
    list_filter = ('difficulty', 'status', 'created_at', 'category')  # Add filters for difficulty, status, and category
    search_fields = ('title', 'created_by__username')  # Allow searching by title or creator's username
    ordering = ('-created_at',)  # Order projects by the newest first
    date_hierarchy = 'created_at'  # Add a date hierarchy for easier navigation
    autocomplete_fields = ['category']  # Enable autocomplete for category selection


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'skill_level', 'status', 'created_at')  # Key fields in list view
    list_filter = ('skill_level', 'status', 'created_at', 'category')  # Filters for skill level, status, and category
    search_fields = ('title', 'created_by__username')  # Search by title or creator's username
    ordering = ('-created_at',)  # Newest tutorials first
    prepopulated_fields = {'title': ('content',)}  # Auto-generate fields for SEO or internal links


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Display category name and description
    search_fields = ('name',)  # Enable search by category name
    ordering = ('name',)  # Alphabetical order by name


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'tutorial')  # Show which user favorited which tutorial
    list_filter = ('user',)  # Filter by user
    autocomplete_fields = ['user', 'tutorial']  # Enable autocomplete for user and tutorial fields
    ordering = ('user',)  # Order by user
