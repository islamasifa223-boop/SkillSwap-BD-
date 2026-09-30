from django.contrib import admin
from .models import Profile, Skill, ExchangeRequest


admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(ExchangeRequest)