from django.contrib import admin

from jobs.models import Job, Customer


# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_code','description')
    search_fields = ('job_code',)
    list_filter = ('job_code',)
    filter_horizontal = ('labels',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)