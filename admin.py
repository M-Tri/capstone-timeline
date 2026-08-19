from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Opinion, Label, Article, Image, Supervise

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Opinion)
admin.site.register(Label)
admin.site.register(Article)
admin.site.register(Image)
admin.site.register(Supervise)