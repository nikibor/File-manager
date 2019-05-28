from django import forms


class CreateFolderForm(forms.Form):
    """
    Форма создания новой папки
    """
    folder_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2 mb-sm-0',
                'placeholder': 'Новая папка'}),
        label=False,
        required=False)
    redirect_link = forms.CharField(widget=forms.HiddenInput())


class UploadFileForm(forms.Form):
    """
    Форма загрузки нового файла
    """
    file = forms.FileField(required=False, label=False)
    redirect_link = forms.CharField(widget=forms.HiddenInput())


class SearchClassForm(forms.Form):
    """
    Форма поиска по классам
    """
    query = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Введите название класса',
                'style': 'width:80%'}),
        label=False,
        required=False)
    redirect_link = forms.CharField(widget=forms.HiddenInput())
