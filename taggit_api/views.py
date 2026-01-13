# -*- coding: utf-8 -*-

from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from taggit.models import Tag
from taggit.models import TaggedItem


class CanAddTag(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('taggit.add_tag')


class CanDeleteTag(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('taggit.delete_tag')


class RemoveTagApi(APIView):
    permission_classes = [IsAuthenticated, CanDeleteTag]

    def delete(self, request, app_label=None, model_name=None, obj_id=None, tag_id=None, tag_slug=None):
        if tag_id:
            lookup = dict(pk=tag_id)
        else:
            lookup = dict(slug=tag_slug)

        try:
            tag = Tag.objects.get(**lookup)
        except Tag.DoesNotExist:
            raise Http404('Tag not found: {}'.format(tag_id))

        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        except ContentType.DoesNotExist:
            raise Http404('Model not found: {}.{}'.format(app_label, model_name))

        if obj_id is not None:
            try:
                obj = content_type.get_object_for_this_type(pk=obj_id)
            except ObjectDoesNotExist:
                raise Http404(f'Object not found: {app_label}.{model_name}: {obj_id}')

            # FIXME: The tag-manager could be named different than 'tags'.
            try:
                obj.tags.remove(tag)
            except AttributeError as exc:
                raise ImproperlyConfigured(f'Object is not taggible: {exc}')

        else:
            TaggedItem.objects.filter(content_type=content_type, tag=tag).delete()

        # Cleanup tag if no tagged-items left.
        if not TaggedItem.objects.filter(tag=tag):
            tag.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AddTagApi(APIView):
    permission_classes = [IsAuthenticated, CanAddTag]

    def post(self, request, app_label=None, model_name=None, obj_id=None, tag_id=None, tag_slug=None):
        if tag_id:
            try:
                tag = Tag.objects.get(pk=tag_id)
            except Tag.DoesNotExist:
                raise Http404(f'Tag not found: {tag_id}')
        else:
            tag, _ = Tag.objects.get_or_create(slug=tag_slug, defaults=dict(name=tag_slug))

        try:
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        except ContentType.DoesNotExist:
            raise Http404(f'Model not found: {app_label}.{model_name}')

        try:
            obj = content_type.get_object_for_this_type(pk=obj_id)
        except ObjectDoesNotExist:
            raise Http404(f'Object not found: {app_label}.{model_name}: {obj_id}')

        # FIXME: The tag-manager could be named different than 'tags'.
        try:
            obj.tags.add(tag)
        except AttributeError as exc:
            raise ImproperlyConfigured(f'Object is not taggible: {exc}')

        return Response(status=status.HTTP_204_NO_CONTENT)
