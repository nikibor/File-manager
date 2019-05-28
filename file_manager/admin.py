from django.contrib import admin

# Register your models here.
from file_manager.models import Classified, ImgClass


class ClassifiedAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'path',
    ]
    list_filter = ['img_class']


class ImgClassAdmin(admin.ModelAdmin):
    list_display = [
        'title'
    ]


admin.site.register(Classified, ClassifiedAdmin)
admin.site.register(ImgClass, ImgClassAdmin)
