import os
import shutil

import numpy as np
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.shortcuts import render
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.preprocessing import image

from app import settings
from file_manager.forms import CreateFolderForm, UploadFileForm
from file_manager.processes.content import Content
from file_manager.processes.links import LinksUtil


def index_page(request):
    """
    Титульная страница приложения, открывающая начальную дирректорию
    """
    files = Content.generate_folder_links(settings.START_FOLDER)
    response = {
        'files': files,
        'folder_form': CreateFolderForm(data={'redirect_link': '/'}),
        'file_form': UploadFileForm(data={'redirect_link': '/'})
    }
    return render(request, 'file_manager/home.html', response)


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
    folder_path = '{}/{}'.format(settings.START_FOLDER, path.replace('+', '/'))

    model = ResNet50(weights='imagenet')

    img = image.load_img(folder_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)

    preds = model.predict(x)
    answers = decode_predictions(preds, top=10)[0]
    for answer in answers:
        print(answer)
    data = {
        'image': folder_path,
        'classes': answers
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
