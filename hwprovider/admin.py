from django.contrib import admin
from django.contrib.auth.models import Group
from .models import HomeWorkManager, HomeWork
from .forms import HomeWorkManagerForm

admin.site.unregister(Group)


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    readonly_fields = ['email', 'homework_num', 'date']


@admin.register(HomeWorkManager)
class HomeWorkManagerAdmin(admin.ModelAdmin):
    form = HomeWorkManagerForm

