# -*- coding: utf-8 -*-

from django.db import models
from taggit.managers import TaggableManager


class ModelA(models.Model):
    id = models.AutoField(primary_key=True)
    tags = TaggableManager(blank=True)


class ModelB(models.Model):
    id = models.AutoField(primary_key=True)
    tags = TaggableManager(blank=True)
