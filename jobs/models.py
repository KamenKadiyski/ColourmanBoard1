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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='jobs')

    def __str__(self):
        return f'{self.job_code} - {self.description}'
