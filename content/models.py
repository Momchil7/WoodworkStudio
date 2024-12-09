from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from core.models import User


class Category(models.Model):
    """
    Categories for Projects or Tutorials (e.g., Furniture, Carving, Tools).
    """
    CATEGORY_CHOICES = [
        ('tables', 'Tables'),
        ('chairs', 'Chairs'),
        ('beds', 'Beds'),
        ('wardrobes', 'Wardrobes'),
        ('couches', 'Couches'),
        ('kitchens', 'Kitchens'),
        ('decorative', 'Decorative'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.get_name_display()


class Project(models.Model):
    """
    Woodworking Project model.
    """
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    materials_used = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    images = models.ImageField(upload_to='projects/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projects')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Tutorial(models.Model):
    """
    Tutorials for woodworking skills and techniques.
    """
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    video_link = models.URLField(blank=True, null=True)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutorials')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved')], default='pending')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tutorials')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    """
    Allows users to bookmark tutorials they want to revisit.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='favorited_by')

    def __str__(self):
        return f"{self.user.username} favorited {self.tutorial.title}"
