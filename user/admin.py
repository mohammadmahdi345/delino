from django.contrib import admin
from .models import User, Comment, Gateway

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Gateway)