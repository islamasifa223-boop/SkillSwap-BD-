from django import forms
from .models import Profile
from .models import Skill
from .models import ExchangeRequest
from django import forms
from .models import Profile
from .models import Session
from .models import Review

class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            'profile_image',
            'bio',
            'location',
            'facebook',
            'linkedin'
        ]

        
class SkillForm(forms.ModelForm):

    class Meta:
        model = Skill

        fields = [
            'title',
            'category',
            'skill_type',
            'description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill title'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter category'}),
            'skill_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter skill description'}),
        }

        
class ExchangeRequestForm(forms.ModelForm):

    class Meta:

        model = ExchangeRequest

        fields = ['message']



class SessionForm(forms.ModelForm):

    class Meta:
        model = Session

        fields = [
            'session_date',
            'session_time',
            'meeting_link'
        ]

        widgets = {
            'session_date': forms.DateInput(attrs={'type': 'date'}),
            'session_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            'rating',
            'comment'
        ]