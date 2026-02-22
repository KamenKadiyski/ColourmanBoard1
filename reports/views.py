from django.shortcuts import render, get_object_or_404
from .models  import ReportConfiguration
from django.http import HttpRequest, HttpResponse
from .reports_logic import ReportLibrary
from .forms import DynamicReportForm


# Create your views here.

def report_list(request):
    page_title = 'Reports'
    nav_path = 'shared/navigation.html'

    reports = ReportConfiguration.objects.filter(is_active=True)
    context = {
        'reports': reports,
        'page_title': page_title,
        'nav_path': nav_path
    }
    return render(request, 'reports/report_list.html', context)


def report_view(request: HttpRequest, report_slug: str) -> HttpResponse:
    page_title = 'Report'
    nav_path = 'shared/navigation.html'

    rep_config = get_object_or_404(ReportConfiguration, slug=report_slug)
    result = None
    if  request.GET:
        form = DynamicReportForm(rep_config, request.POST or request.GET)
        if form.is_valid():
            method = getattr(ReportLibrary, rep_config.method_name)
            result = method(**form.cleaned_data)
    else:
        form = DynamicReportForm(rep_config)
    context = {
        'form': form,
        'result': result,
        'config' : rep_config,
        'page_title': page_title,
        'nav_path': nav_path,

    }

    return render(request, 'reports/report.html', context)



