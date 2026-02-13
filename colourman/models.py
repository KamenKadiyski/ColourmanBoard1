from datetime import date

from django.db import models



# Create your models here.
#Модел за служителя отговорен за печата или слагане на етикети за поръчките
class Colourman(models.Model):
    clock_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    shift = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.clock_number} - {self.name}"
#Модел за описване на ползване на етикетите или бланките за етикети.
class PrintingLog(models.Model):
    colourman = models.ForeignKey(Colourman, on_delete=models.CASCADE)
    code = models.ForeignKey('jobs.Job', on_delete=models.CASCADE)
    label = models.ForeignKey('labels.Label', on_delete=models.CASCADE)
    amount = models.IntegerField()
    usage_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.colourman} - {self.code} - {self.label} - {self.amount}"

#Описва всички установени проблеми с качеството на етикетите
class Unacceptable(models.Model):
    colourman = models.ForeignKey(Colourman, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.colourman} - {self.reason}"