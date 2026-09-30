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
            'bio',
            'skills',
            'profile_image'
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
        
class ExchangeRequestForm(forms.ModelForm):

    class Meta:

        model = ExchangeRequest

        fields = ['message']

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