import os
from typing import List

from bia_prev import settings


class LinksUtil:

    @staticmethod
    def generate_folder_link(dir_name: str, file_name=None) -> str:
        if file_name:
            file_path = os.path.join(dir_name, file_name)
        else:
            file_path = dir_name
        link = file_path.replace('/', '+')
        link = link.replace('app+static+'.format(settings.START_FOLDER), '')
        return link

    @staticmethod
    def generate_path_links(current_folder: str) -> List:
        folders_in_path = current_folder.split('/')
        folders_in_path.remove('static')
        folders_in_path.remove('app')
        links = []
        pos = len(folders_in_path)
        for i in range(len(folders_in_path)):
            path = ''
            for j in range(len(folders_in_path) - pos):
                path += folders_in_path[j]
            links.append(
                {
                    'link': LinksUtil.generate_folder_link(path),
                    'name': folders_in_path[i]
                })
            pos -= 1
        return links

    @staticmethod
    def get_path_from_link(file_link: str) -> str:
        return '{}/{}'.format(settings.START_FOLDER,
                              file_link.replace('+', '/'))
