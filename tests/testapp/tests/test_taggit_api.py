

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.models import Tag
from taggit_api import __version__, apps
from testapp.models import ModelA
from testapp.models import ModelB
from testapp.management.commands.createtestdata import create_test_data


class TaggitApiTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def setUp(self):
        self.admin = User.objects.get(username='admin')
        self.client.force_login(self.admin)
        self.url = reverse('admin:testapp_modela_changelist')

    def test_01_remove_tag_from_all_by_id(self):
        # Remove tag from all ModelA objects.
        tag1 = Tag.objects.get(name='one')
        url = reverse('remove-tag-from-all-by-id', kwargs=dict(tag_id=tag1.id, app_label='testapp', model_name='modela'))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 204)
        objs_by_tag = ModelA.objects.filter(tags__name__in=[tag1.name])
        self.assertEqual(len(objs_by_tag), 0)
        self.assertFalse(objs_by_tag)
        self.assertRaises(Tag.DoesNotExist, Tag.objects.get, pk=tag1.id)

        # Remove tag that's linked with objects of two different models.
        tag2 = Tag.objects.get(name='two')
        ModelB.objects.get(pk=1).tags.add(tag2.name)
        url = reverse('remove-tag-from-all-by-id', kwargs=dict(tag_id=tag2.id, app_label='testapp', model_name='modela'))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 204)
        objs_by_tag = ModelA.objects.filter(tags__name__in=[tag2.name])
        self.assertEqual(len(objs_by_tag), 0)
        self.assertFalse(objs_by_tag)
        self.assertTrue(Tag.objects.get(pk=tag2.id))
        self.assertTrue(Tag.objects.get(pk=tag2.id))

        # Unkown tag-id.
        url = reverse('remove-tag-from-all-by-id', kwargs=dict(tag_id=1234, app_label='testapp', model_name='modela'))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 404)

        # Unkown model.
        url = reverse('remove-tag-from-all-by-id', kwargs=dict(tag_id=tag2.id, app_label='testapp', model_name='dummy'))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 404)

    def test_02_remove_tag_from_all(self):
        # Remove tag from all ModelA objects.
        tag1 = Tag.objects.get(name='one')
        url = reverse('remove-tag-from-all', kwargs=dict(tag_slug=tag1.slug, app_label='testapp', model_name='modela'))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 204)
        objs_by_tag = ModelA.objects.filter(tags__name__in=[tag1.name])
        self.assertEqual(len(objs_by_tag), 0)
        self.assertFalse(objs_by_tag)
        self.assertRaises(Tag.DoesNotExist, Tag.objects.get, pk=tag1.id)

    def test_03_remove_tag_by_id(self):
        # Remove tag from a ModalA object.
        tag1 = Tag.objects.get(name='one')
        obj, ref_obj = ModelA.objects.filter(tags__name__in=[tag1.name])[:2]
        url = reverse('remove-tag-by-id', kwargs=dict(tag_id=tag1.id, app_label='testapp', model_name='modela', obj_id=obj.id))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 204)
        obj_tags = obj.tags.all()
        self.assertNotIn(tag1, obj_tags)
        ref_tags = ref_obj.tags.all()
        self.assertIn(tag1, ref_tags)

        # Unkown obj-id.
        url = reverse('remove-tag-by-id', kwargs=dict(tag_id=tag1.id, app_label='testapp', model_name='modela', obj_id=9999))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 404)

    def test_04_remove_tag(self):
        # Remove tag from a ModalA object.
        tag1 = Tag.objects.get(name='one')
        obj = ModelA.objects.filter(tags__name__in=[tag1.name]).first()
        url = reverse('remove-tag', kwargs=dict(tag_slug=tag1.slug, app_label='testapp', model_name='modela', obj_id=obj.id))
        resp = self.client.delete(url, follow=True)
        self.assertEqual(resp.status_code, 204)
        obj_tags = obj.tags.all()
        self.assertNotIn(tag1, obj_tags)

    def test_05_add_tag_by_id(self):
        # Add tag to a ModalA object.
        tag1 = Tag.objects.get(name='one')
        obj = ModelA.objects.all().first()
        obj.tags.remove(tag1)
        url = reverse('add-tag-by-id', kwargs=dict(tag_id=tag1.id, app_label='testapp', model_name='modela', obj_id=obj.id))
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 204)
        obj_tags = obj.tags.all()
        self.assertIn(tag1, obj_tags)

        # Unkown tag-id.
        url = reverse('add-tag-by-id', kwargs=dict(tag_id=9999, app_label='testapp', model_name='modela', obj_id=obj.id))
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 404)

        # Unkown model.
        url = reverse('add-tag-by-id', kwargs=dict(tag_id=tag1.id, app_label='testapp', model_name='unkown', obj_id=obj.id))
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 404)

        # Unkown obj-id.
        url = reverse('add-tag-by-id', kwargs=dict(tag_id=tag1.id, app_label='testapp', model_name='modela', obj_id=9999))
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 404)

    def test_06_add_tag(self):
        # Add tag to a ModalA object.
        tag1 = Tag.objects.get(name='one')
        obj = ModelA.objects.all().first()
        obj.tags.remove(tag1)
        url = reverse('add-tag', kwargs=dict(tag_slug=tag1.slug, app_label='testapp', model_name='modela', obj_id=obj.id))
        resp = self.client.post(url, follow=True)
        self.assertEqual(resp.status_code, 204)
        obj_tags = obj.tags.all()
        self.assertIn(tag1, obj_tags)
