from django.db import models


# Create your models here.

class ImgClass(models.Model):
    title = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.title


class Classified(models.Model):
    name = models.CharField(max_length=255, null=False)
    path = models.CharField(max_length=400, null=False)
    img_class = models.ManyToManyField(ImgClass)

    def __str__(self):
        return self.name
