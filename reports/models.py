from django.db import models
from django.apps import apps


class ReportConfiguration(models.Model):
    name = models.CharField(max_length=255,verbose_name='Report name')
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    method_name = models.CharField(max_length=255,
                                   help_text='function name in reports library')

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ReportParameter(models.Model):
    PARAMETER_TYPES = (
        ('date', 'Date'),
        ('int', 'Integer'),
        ('str', 'String'),
        ('choice', 'Choice'),
        ('bool', 'Boolean'),
    )
    report = models.ForeignKey(ReportConfiguration, on_delete=models.CASCADE,related_name='parameters')
    name = models.CharField(max_length=255, help_text='Parameter name into function')
    label = models.CharField(max_length=255, help_text='Parameter label for the user')
    parameter_type = models.CharField(max_length=10, choices=PARAMETER_TYPES,
                                      help_text='Parameter type')
    source_model = models.CharField(max_length=50,
                                    blank=True, null=True,
                                    help_text='app_label.ModelName for choice parameters')
    is_required = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.label} for {self.report.name}"