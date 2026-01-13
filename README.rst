============================
Welcome to django-taggit-api
============================

.. image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue
   :target: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue
   :alt: python: 3.8, 3.9, 3.10,3.11, 3.12, 3.13

.. image:: https://img.shields.io/badge/django-3.2%20%7C%204.0%20%7C%204.1%20%7C%204.2%20%7C%205.0%20%7C%205.1%20%7C%205.2%20%7C%206.0-orange
   :target: https://img.shields.io/badge/django-3.2%20%7C%204.0%20%7C%204.1%20%7C%204.2%20%7C%205.0%20%7C%205.1%20%7C%205.2%20%7C%206.0-orange
   :alt: django: 3.2, 4.0, 4.1, 4.2, 5.0, 5.1, 5.2, 6.0

.. image:: https://github.com/thomst/django-taggit-api/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/thomst/django-taggit-api/actions/workflows/ci.yml
   :alt: Run tests for django-taggit-api

.. image:: https://coveralls.io/repos/github/thomst/django-taggit-api/badge.svg?branch=main
   :target: https://coveralls.io/github/thomst/django-taggit-api?branch=main
   :alt: Coveralls


Description
===========
This application provides a simple url-path based api for django-taggit to add
or remove tags.

The api is best described by the url-patterns itself:

Remove a tag from all objects of a model using the tag-id or -slug::

    'remove-tag/<int:tag_id>/from/<slug:app_label>/<slug:model_name>/'
    'remove-tag/<slug:tag_slug>/from/<slug:app_label>/<slug:model_name>/'

Remove a tag from a single object using the tag-id or -slug::

    'remove-tag/<int:tag_id>/from/<slug:app_label>/<slug:model_name>/<int:obj_id>/'
    'remove-tag/<slug:tag_slug>/from/<slug:app_label>/<slug:model_name>/<int:obj_id>/'

Add a tag to an object using the tag-id or -slug::

    'add-tag/<int:tag_id>/to/<slug:app_label>/<slug:model_name>/<int:obj_id>/'
    'add-tag/<slug:tag_slug>/to/<slug:app_label>/<slug:model_name>/<int:obj_id>/'


Installation
============
Install from pypi.org::

    pip install django-taggit-api


Setup
=====
Add :code:`taggit_api` to your installed apps::

    INSTALLED_APPS = [
        'taggit_api',
        ...
    ]

Extend your :code:`url_patterns` in urls.py::

    urlpatterns = [
        ...
        path('api/', include('taggit_api.urls')),
    ]
