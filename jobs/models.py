from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    only_preprinted_labels = models.BooleanField(default=False)
    only_customer_colours = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Job(models.Model):
    job_code = models.CharField(max_length=20, unique=True)

    description = models.CharField(max_length=200)
    labels = models.ManyToManyField('labels.Label', related_name='jobs')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customers')
    # баркода ще зависи от етикета - напечатан - ще взима баркода от етикета
    # ако е бланка ще се ползва баркода от полето, може да се задава в последствие
    # ако ще се слага нов етикет - баркодовете трябва да са еднакви ако е preprinted.
    barcode = models.CharField(max_length=15, default='5038135000000')

    def __str__(self):
        return f'{self.job_code} - {self.description}'
