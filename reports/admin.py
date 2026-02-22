from django.contrib import admin

from reports.models import ReportConfiguration, ReportParameter


# Register your models here.

@admin.register(ReportConfiguration)
class ReportConfigurationAdmin(admin.ModelAdmin):
    pass


@admin.register(ReportParameter)
class ReportParameterAdmin(admin.ModelAdmin):
    pass
