from django import forms


class CreateFolderForm(forms.Form):
    folder_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-2 mr-sm-2 mb-sm-0',
                'placeholder': 'Новая папка'}),
        label=False,
        required=False)
    redirect_link = forms.CharField(widget=forms.HiddenInput())


class UploadFileForm(forms.Form):
    file = forms.FileField(required=False, label=False)
    redirect_link = forms.CharField(widget=forms.HiddenInput())
