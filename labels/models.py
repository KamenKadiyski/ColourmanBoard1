from django.db import models

from jobs.models import Job


# Create your models here.
class LabelSize(models.Model):
    size = models.CharField(max_length=10)
    usage = models.TextField()


    def __str__(self):
        return self.size
    
class LabelType(models.Model):
    name = models.CharField(max_length=100)
    sizes = models.ManyToManyField(LabelSize, related_name='label_types')
    is_preprinted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Label(models.Model):

    bar_code = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    label_types = models.ManyToManyField(LabelType, related_name='labels')
    image = models.ImageField(upload_to='images/', blank=True, null=True)


    def __str__(self):
        return self.description
