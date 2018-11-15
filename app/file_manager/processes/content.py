import os
from typing import List

from django.http import HttpResponse

from file_manager.processes.links import LinksUtil


class Content:

    @staticmethod
    def generate_folder_links(start_position: str) -> List:
        file_names = os.listdir(start_position)
        file_links = []
        for f_name in file_names:
            file_links.append(
                LinksUtil.generate_folder_link(start_position, f_name))
        files = []
        for i in range(len(file_names)):
            files.append({
                'name': file_names[i],
                'link': file_links[i],
                'size': get_file_size(
                    os.path.join(start_position, file_names[i]))
            })
        return files

    @staticmethod
    def generate_file_response(file_path: str) -> HttpResponse:
        response = HttpResponse(
            content_type='application/{}'.format(file_path.split('.')[-1]))
        response[
            'Content-Disposition'] = 'attachment; filename="{}"'.format(
            file_path)
        return response


def get_file_size(file_path: str) -> float:
    return round(os.stat(file_path).st_size / 1024, 2)
