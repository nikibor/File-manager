from django.urls import path

from . import views

urlpatterns = [
    path('<path>', views.base_page, name='folder_page'),
    path('', views.index_page, name='base_page'),
    path('delete/<path>',views.delete, name='delete'),
    path('new_folder/', views.create_folder, name='create_folder'),
    path('upload_file/', views.upload_file, name='upload_file')
]
