from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')  # Display key fields in the list view
    list_filter = ('role', 'is_staff', 'is_superuser')  # Add filters for roles and permissions
    search_fields = ('username', 'email')  # Enable searching by username and email
    ordering = ('username',)  # Default ordering by username
    fieldsets = (  # Organize the form layout for editing a user
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'profile_picture', 'bio')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_superuser')}),
    )
