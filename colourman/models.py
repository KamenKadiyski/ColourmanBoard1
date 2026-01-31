from django.db import models
from django.db.models.functions import datetime


# Create your models here.
class Colourman(models.Model):
    clock_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    shift = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.clock_number} - {self.name}"

class PrintingLog(models.Model):
    colourman = models.ForeignKey(Colourman, on_delete=models.CASCADE)
    code = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    label = models.ForeignKey('labels.Label', on_delete=models.CASCADE)
    label_type = models.ForeignKey('labels.LabelType', on_delete=models.CASCADE)
    label_size = models.ForeignKey('labels.LabelSize', on_delete=models.CASCADE)
    amount = models.IntegerField()


    def __str__(self):
        return f"{self.colourman} - {self.code} - {self.label} - {self.amount}"


class Unacceptable(models.Model):
    colourman = models.ForeignKey(Colourman, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.colourman} - {self.reason}"