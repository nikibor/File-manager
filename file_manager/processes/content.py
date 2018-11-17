import os
from typing import List

from django.http import HttpResponse

from file_manager.processes.links import LinksUtil


class Content:
    """
    Шаблоны, возвращающие информацию о положении объектов в системе
    """

    @staticmethod
    def generate_folder_links(start_position: str) -> List:
        """
        Создание шаблона, который будет передан для отрисовки содержимого дирректории
        :param start_position: текущая дирректория
        :return: список всех объектов в дирректории
        """
        file_names = os.listdir(start_position)
        file_links = []
        for f_name in file_names:
            file_links.append(
                LinksUtil.generate_folder_link(start_position, f_name))
        files = []
        for i in range(len(file_names)):
            is_folder = '.' not in file_names[i]
            files.append({
                'name': file_names[i],
                'link': file_links[i],
                'size': get_file_size(
                    os.path.join(start_position, file_names[i]), is_folder)
            })
        return files

    @staticmethod
    def generate_file_response(file_path: str) -> HttpResponse:
        """
        Шаблон для возвращения файла пользователю
        :param file_path: путь до файла
        :return: Http ответ, содержащий всю информацию о файле
        """
        response = HttpResponse(
            content_type='application/{}'.format(file_path.split('.')[-1]))
        response[
            'Content-Disposition'] = 'attachment; filename="{}"'.format(
            file_path)
        return response


def get_file_size(file_path: str, is_folder) -> float:
    """
    Получение размера файла в килобайтах
    :param file_path: путь до файла
    :return: размер файла
    """
    if is_folder:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(file_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
    else:
        total_size = os.stat(file_path).st_size
    return round(total_size / 1024, 2)
