from django.contrib import admin

from colourman.models import Colourman,PrintingLog


# Register your models here.
@admin.register(Colourman)
class ColourmanAdmin(admin.ModelAdmin):
    list_display = ('clock_number', 'name', 'shift')
    list_filter = ('shift',)
    search_fields = ('clock_number',)


@admin.register(PrintingLog)
class PrintingLogAdmin(admin.ModelAdmin):
    list_display = ('colourman', 'code', 'label', 'label_type', 'label_size', 'amount')
    search_fields = ('label__description', 'colourman__clock_number', 'code__job_code')
    list_filter = ('colourman', 'label_type', 'label_size')