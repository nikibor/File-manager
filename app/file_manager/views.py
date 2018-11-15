import os
import shutil

from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.shortcuts import render

from bia_prev import settings
from file_manager.forms import CreateFolderForm, UploadFileForm
from file_manager.processes.content import Content
from file_manager.processes.links import LinksUtil


def index_page(request):
    files = Content.generate_folder_links(settings.START_FOLDER)
    response = {
        'files': files,
        'folder_form': CreateFolderForm(data={'redirect_link': '/'}),
        'file_form': UploadFileForm(data={'redirect_link': '/'})
    }
    return render(request, 'file_manager/home.html', response)


def base_page(request, path: str):
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
    folder_path = '{}/{}'.format(settings.START_FOLDER, path.replace('+', '/'))
    redirect_link = '+'.join(folder_path.split('/')[2:-1])
    if '.' in folder_path:
        os.remove(folder_path)
    else:
        shutil.rmtree(folder_path)
    return redirect('/{}'.format(redirect_link))


def upload_file(request):
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
