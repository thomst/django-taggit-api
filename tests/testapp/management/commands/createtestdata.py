# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from testapp.models import ModelA
from testapp.models import ModelB


def create_test_data():
    try:
        User.objects.create_superuser(
            'admin',
            'admin@testapp.org',
            'adminpassword')
    except IntegrityError:
        pass

    # clear existing data
    ModelA.objects.all().delete()

    # Create tagged objects.
    for i in range(12):

        a_obj = ModelA(id=i)
        a_obj.save()
        if i % 2:
            a_obj.tags.add('one', 'two')

        b_obj = ModelB(id=i)
        b_obj.save()
        if i % 3:
            b_obj.tags.add('two')


class Command(BaseCommand):
    help = 'Create test data.'

    def handle(self, *args, **options):
        create_test_data()
