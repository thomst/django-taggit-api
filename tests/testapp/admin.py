# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import ModelA
from .models import ModelB


@admin.register(ModelA)
class ModelAAdmin(admin.ModelAdmin):
    list_display = ('id',)


@admin.register(ModelB)
class ModelAAdmin(admin.ModelAdmin):
    list_display = ('id',)
