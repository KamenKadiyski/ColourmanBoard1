from django.contrib import admin

from jobs.models import Job
from labels.models import LabelSize, Label, LabelType


# Register your models here.
@admin.register(LabelSize)
class LabelSizeAdmin(admin.ModelAdmin):
    list_display = ('size', 'usage')
    search_fields = ('size',)
    list_filter = ('size',)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('bar_code', 'description',)
    search_fields = ('jobs__job_code',)
    filter_horizontal = ('label_types',)

@admin.register(LabelType)
class LabelTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_preprinted')
    search_fields = ('name',)
    list_filter = ('is_preprinted',)
    filter_horizontal = ('sizes',)
