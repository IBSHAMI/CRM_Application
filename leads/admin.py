from django.contrib import admin
from .models import Lead, Agent, User, UserProfile

# Register your models here.
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(User)
admin.site.register(UserProfile)


