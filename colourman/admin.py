from django.contrib import admin

from colourman.models import Colourman, PrintingLog, Unacceptable


# Register your models here.
@admin.register(Colourman)
class ColourmanAdmin(admin.ModelAdmin):
    list_display = ('clock_number', 'name', 'shift')
    list_filter = ('shift',)
    search_fields = ('clock_number',)


@admin.register(PrintingLog)
class PrintingLogAdmin(admin.ModelAdmin):
    list_display = ('colourman', 'code', 'label', 'amount')
    search_fields = ('label__description', 'colourman__clock_number', 'code__job_code')
    list_filter = ('colourman', )



@admin.register(Unacceptable)
class UnacceptableAdmin(admin.ModelAdmin):
    list_display = ('colourman','reason')
    search_fields = ('colourman__clock_number','colourman__name','colourman__shift')
    list_filter = ('colourman__clock_number','colourman__name',)