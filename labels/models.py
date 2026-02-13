from django.db import models

from jobs.models import Job


# Create your models here.

#Модел за възможните размери на етиктите
class LabelSize(models.Model):
    size = models.CharField(max_length=10)
    usage = models.TextField()


    def __str__(self):
        return self.size



#Модлеът описва типовете етикети
class LabelType(models.Model):
    name = models.CharField(max_length=100)
    sizes = models.ManyToManyField(LabelSize, related_name='label_types')
    is_preprinted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
#Моделът описва самият етикет
class Label(models.Model):
    #ако етикета е preprinted - задължително трябва да има баркод, ако е бланка - празно.
    bar_code = models.CharField(max_length=15, null=True, blank=True)
    description = models.CharField(max_length=100)
    label_types = models.ManyToManyField(LabelType, related_name='labels')
    image = models.ImageField(upload_to='images/', blank=True, null=True)


    def __str__(self):
        return self.description
