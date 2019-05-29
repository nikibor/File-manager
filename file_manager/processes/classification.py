import os

from app.settings import START_FOLDER
from darknet.python.darknet import yolo_image
from file_manager.models import Classified, ImgClass


class FileClassifier:

    @staticmethod
    def classify_all():
        for path, subdirs, files in os.walk(START_FOLDER):
            for name in files:
                if 'classified' in name:
                    continue
                extension = name.split('.')[-1]
                if extension.lower() not in ['gif', 'jpg', 'peg', 'tiff',
                                             'png']:
                    continue
                file_path = os.path.join(path, name)
                new_path, classes = yolo_image(file_path, folder='classified')
                if len(classes[0]) == 0:
                    continue
                img = Classified(name=name, path=new_path)
                img.save()
                for cat in classes[0]:
                    img_class = str(cat[0].decode('utf-8'))
                    try:
                        cathegory = ImgClass.objects.get(title=img_class)
                        img.img_class.add(cathegory)
                        img.save()
                    except Exception:
                        continue
        return "OK"
