import os
import shutil

from django.test import TestCase

from bia_prev import settings
from file_manager.processes.content import Content
from file_manager.processes.links import LinksUtil


class FileManagerTestCase(TestCase):

    def test_generate_link(self):
        os.mkdir('{}/for_test'.format(settings.START_FOLDER))
        os.mkdir('{}/for_test/1'.format(settings.START_FOLDER))
        os.mkdir('{}/for_test/2'.format(settings.START_FOLDER))
        result = Content.generate_folder_links(
            '{}/for_test'.format(settings.START_FOLDER))
        shutil.rmtree('{}/for_test'.format(settings.START_FOLDER))
        self.assertEqual(result, [
            {'name': '1', 'link': 'for_test+1'},
            {'name': '2', 'link': 'for_test+2'}
        ])

    def test_generate_path(self):
        os.mkdir('{}/for_test'.format(settings.START_FOLDER))
        os.mkdir('{}/for_test/1'.format(settings.START_FOLDER))
        os.mkdir('{}/for_test/1/2'.format(settings.START_FOLDER))
        result = LinksUtil.generate_path_links(
            '{}/for_test/1/2'.format(settings.START_FOLDER))
        shutil.rmtree('{}/for_test'.format(settings.START_FOLDER))
        self.assertEqual(result, [
            {'link': '', 'name': 'for_test'},
            {'link': 'for_test', 'name': '1'},
            {'link': 'for_test1', 'name': '2'},
        ])

    def test_gen_folder_link(self):
        os.mkdir('{}/for_test'.format(settings.START_FOLDER))
        os.mkdir('{}/for_test/1'.format(settings.START_FOLDER))
        os.mkdir('{}/for_test/1/2'.format(settings.START_FOLDER))
        result = LinksUtil.generate_folder_link(
            '{}/for_test/1/2'.format(settings.START_FOLDER))
        shutil.rmtree('{}/for_test'.format(settings.START_FOLDER))
        self.assertEqual(result, 'for_test+1+2')
