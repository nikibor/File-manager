import os
import shutil

import keras
import numpy as np
from app.settings import START_FOLDER
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.shortcuts import render
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.preprocessing import image

from app import settings
from darknet.python.darknet import yolo_image
from file_manager.forms import CreateFolderForm, UploadFileForm, SearchClassForm
from file_manager.models import Classified, ImgClass
from file_manager.processes.classification import FileClassifier
from file_manager.processes.content import Content
from file_manager.processes.links import LinksUtil


# todo: 1. Добавить Celery для управления и просмотра нагрузки
# todo: 2. Настроить докер контейнеры с запуском тестов - стандартные Django + нагрузочное
# todo: 3. Настройка визуала - добавление динамики js
# todo: 4. Добавление поиска: каждый новый загруженный файл автоматичесски классифицируется, при попадании в систему, затем можно выполнить поиск по названию класса
# todo: 5. Хранить и переносить данные о размеченных классах в NoSQL БД - Mongo
# todo: 6. Переписать README.MD
# todo: 7. ElasticSearch + Kibana + Sentry (???)

def file_classification(request):
    if os.path.exists(os.path.join(START_FOLDER, 'classified')):
        shutil.rmtree(os.path.join(START_FOLDER, 'classified'))
    os.mkdir(os.path.join(START_FOLDER, 'classified'))
    Classified.objects.all().delete()
    FileClassifier.classify_all()


def index_page(request):
    """
    Титульная страница приложения, открывающая начальную дирректорию
    """

    files = Content.generate_folder_links(settings.START_FOLDER)
    response = {
        'files': files,
        'folder_form': CreateFolderForm(data={'redirect_link': '/'}),
        'file_form': UploadFileForm(data={'redirect_link': '/'}),
        'search_form': SearchClassForm(data={'redirect_link': '/'})
    }
    return render(request, 'file_manager/home.html', response)


def search(request):
    """
    Генерация новой дирректории, название которой полученно с формы
    """
    search_data = []
    form = SearchClassForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        img_class = form_data.get('query')
        redirect_link = form_data.get('redirect_link')
        try:
            img_cathegory = ImgClass.objects.get(title=img_class)
            result = Classified.objects.filter(img_class=img_cathegory)
            for cat in result:
                search_data.append(
                    {
                        'path': cat.path,
                        'title': cat.name
                    }
                )
            response = {
                'search_form': SearchClassForm(data={'redirect_link': '/'}),
                'images': search_data
            }
            return render(request,
                          'file_manager/search_result.html',
                          response)
        except Exception:
            return redirect(redirect_link)


def base_page(request, path: str):
    """
    Страница возвращающая содержимое внутренних папок или файлы, содержащиеся там
    :param path: относительный путь до объекта
    """
    current_path = LinksUtil.get_path_from_link(path)
    if '.' in current_path:
        response = Content.generate_file_response(current_path)
        return response
    else:
        files = Content.generate_folder_links(current_path)
        path_links = LinksUtil.generate_path_links(current_path)
        response = {
            'files': files,
            'search_form': SearchClassForm(data={'redirect_link': '/'}),
            'folder_links': path_links,
            'folder_form': CreateFolderForm(data={
                'redirect_link':
                    '/{}'.format(LinksUtil.generate_folder_link(current_path))
            }),
            'file_form': UploadFileForm(data={
                'redirect_link':
                    '/{}'.format(LinksUtil.generate_folder_link(current_path))})
        }
        return render(request, 'file_manager/home.html', response)


def create_folder(request):
    """
    Генерация новой дирректории, название которой полученно с формы
    """
    form = CreateFolderForm(request.POST)
    if form.is_valid():
        form_data = form.cleaned_data
        folder_name = form_data.get('folder_name')
        redirect_link = form_data.get('redirect_link')
        current_folder = '{}/{}'.format(settings.START_FOLDER,
                                        redirect_link.replace('+', '/'))
        os.mkdir(os.path.join(current_folder, folder_name))
        return redirect(redirect_link)


def delete(request, path: str):
    """
    Удаление выбранного объекта
    :param path: путь до объекта
    """
    folder_path = '{}/{}'.format(settings.START_FOLDER, path.replace('+', '/'))
    redirect_link = '+'.join(folder_path.split('/')[1:-1])
    if '.' in folder_path:
        os.remove(folder_path)
    else:
        shutil.rmtree(folder_path)
    return redirect('/{}'.format(redirect_link))


def image_classify(request, path: str):
    with keras.backend.get_session().graph.as_default():
        folder_path = '{}/{}'.format(settings.START_FOLDER,
                                     path.replace('+', '/'))
        model = ResNet50(weights='imagenet')

        img = image.load_img(folder_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x)
        answers = decode_predictions(preds, top=10)[0]
        marks = {}
        for answer in answers:
            marks[answer[1]] = answer[2]

        yolo_img_path, _ = yolo_image(folder_path)
        data = {
            'image': folder_path,
            'yolo_image': yolo_img_path,
            'classes': marks
        }
        return render(request, 'file_manager/classiffy_result.html', data)


def upload_file(request):
    """
    Загрузка файла на сервер, в текущую дирректорию
    """
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        form_data = form.cleaned_data
        redirect_link = form_data.get('redirect_link')
        current_folder = '{}/{}'.format(settings.START_FOLDER,
                                        redirect_link.replace('+', '/'))
        fs = FileSystemStorage()
        file = request.FILES['file']
        fs.save(os.path.join(current_folder, file.name), file)
        return redirect(redirect_link)
