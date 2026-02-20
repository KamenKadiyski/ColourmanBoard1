from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum


# Create your models here.
#Модел за служителя отговорен за печата или слагане на етикети за поръчките
class Colourman(models.Model):
    clock_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    shift = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    @property
    def number_of_fails(self):
        fails_count = self.unacceptable.count()
        return fails_count

    @property
    def sum_of_fails_points(self):
        result = self.unacceptable.aggregate(Sum('points')) or 0.0

        sum_of_points = result['points__sum']
        if not sum_of_points:
            sum_of_points = 0.0
        return float(sum_of_points)



    @property
    def list_of_fails(self):
        fails_list = self.unacceptable.all()
        return fails_list

    @property
    def number_of_labels(self):

        labels_count = self.print_usage_log_colourman.count()
        return labels_count


    def __str__(self):
        return f"{self.clock_number} - {self.name}"




#Модел за описване на ползване на етикетите или бланките за етикети.
class PrintingLog(models.Model):
    colourman = models.ForeignKey(Colourman, on_delete=models.CASCADE,related_name='print_usage_log_colourman')
    code = models.ForeignKey('jobs.Job', on_delete=models.CASCADE,related_name='print_usage_log_jobs')
    label = models.ForeignKey('labels.Label', on_delete=models.CASCADE,related_name='print_usage_log_label')
    amount = models.IntegerField()
    usage_date = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.colourman} - {self.code} - {self.label} - {self.amount}"




#Описва всички установени проблеми с качеството на етикетите
class Unacceptable(models.Model):
    colourman = models.ForeignKey(Colourman, on_delete=models.CASCADE, related_name='unacceptable')
    reason = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    points = models.DecimalField(max_digits=2, decimal_places=1,default=0.5, validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    for_investigation = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.colourman} - {self.reason}"