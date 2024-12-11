from django import forms
from .models import Project

from .models import Tutorial

from .models import Favorite

class ProjectForm(forms.ModelForm):
#форма за създаване и редактиране на проекти. клас Meta определя кой е модела.widgets настроят класовете на HTML елементите.
    class Meta:
        model = Project
        fields = ['title', 'description', 'difficulty', 'materials_used', 'category', 'images'
                  ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project title'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class': 'form-control'}),
            'materials_used': forms.Textarea(attrs={'rows': 3, 'cols': 40, 'class': 'form-control'}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False



class TutorialForm(forms.ModelForm):
    # форма за създаване на турориали
    class Meta:
        model = Tutorial
        fields = ['title', 'content', 'video_link', 'skill_level', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter tutorial title'}),
            'content': forms.Textarea(attrs={'rows': 6, 'cols': 50, 'class': 'form-control'}),
            'video_link': forms.TextInput(attrs={'class': 'form-control'}),
            'skill_level': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False



class FavoriteForm(forms.ModelForm):
 # форма за любими
    class Meta:
        model = Favorite
        fields = ['tutorial']



