import os
from typing import List

from app import settings


class LinksUtil:
    """
    Набор функций, работающих с адресным представлением объектов
    """

    @staticmethod
    def generate_folder_link(dir_name: str, file_name=None) -> str:
        """
        Получение ссылки для перехода по дирректориям в системе
        :param dir_name: текущая папка
        :param file_name: название файла
        :return: ссылка на файл
        """
        if file_name:
            file_path = os.path.join(dir_name, file_name)
        else:
            file_path = dir_name
        link = file_path.replace('/', '+')
        link = link.replace('static+'.format(settings.START_FOLDER), '')
        return link

    @staticmethod
    def generate_path_links(current_folder: str) -> List:
        """
        Создание иеррхии ссылок, для возможности быстрого перехода в корневую дирректорию
        :param current_folder: текущая папка
        :return: шаблон с корневыми дирреториями
        """
        folders_in_path = current_folder.split('/')
        folders_in_path.remove('static')
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
        """
        Получение адреса до файла из ссылки
        :param file_link: ссылка на файл
        :return: условный путь до файла
        """
        return '{}/{}'.format(settings.START_FOLDER,
                              file_link.replace('+', '/'))
