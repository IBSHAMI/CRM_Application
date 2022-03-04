from django.contrib import admin
from .models import Lead, Agent, User, Organization, Category

# Register your models here.
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Category)


