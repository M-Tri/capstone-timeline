from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Opinion, Label, Article, Image, Quiz

# Register your models here.
admin.site.register(Opinion)
admin.site.register(Label)
admin.site.register(Article)
admin.site.register(Image)
admin.site.register(Quiz)


class AddEditorUser(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ( ('Permissions', {'fields': ('is_editor',)}),)

# Register with your new custom user layout in admin
admin.site.register(User, AddEditorUser)