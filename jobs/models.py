from django.db import models

from labels.models import Label


# Create your models here.

#Модел за клиенти. За текущото приложени, не е необходимо да се събират повече данни
class Customer(models.Model):
    name = models.CharField(max_length=100)
    only_preprinted_labels = models.BooleanField(default=False)
    only_customer_colours = models.BooleanField(default=False)

    def __str__(self):
        return self.name


#Дефинира модела за работите. При развитие на приложението, ще се добавят още данни.
#Ще се добавят модели за цветове, матрици, машини.
class Job(models.Model):
    job_code = models.CharField(max_length=20, unique=True)

    description = models.CharField(max_length=200)
    #Един етикет може да бъде на много работи. На една работа може да се използва и етикет алтернатива
    labels = models.ManyToManyField('labels.Label', related_name='jobs')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customers')
    # баркода ще зависи от етикета - напечатан - ще взима баркода от етикета
    # ако е бланка ще се ползва баркода от полето, може да се задава в последствие
    # ако ще се слага нов етикет - баркодовете трябва да са еднакви ако е preprinted.
    barcode = models.CharField(max_length=15, default='5038135000000')
    is_active = models.BooleanField(default=True)


    @property
    def linked_labels(self):
        qs = Label.objects.prefetch_related('jobs')
        return qs


    def __str__(self):
        return f'{self.job_code} - {self.description}'
