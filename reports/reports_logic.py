from django.db.models import Sum, Count
from colourman.models import PrintingLog, Colourman, Unacceptable
from labels.models import Label
from jobs.models import Job

class ReportLibrary:
    @staticmethod
    def label_usage_log(label_id: int, start_date=None, end_date=None, is_preprinted=None):
        logs = PrintingLog.objects.filter(label_id=label_id)
        if start_date:
            logs = logs.filter(date__gte=start_date)
        if end_date:
            logs = logs.filter(date__lte=end_date)
        if is_preprinted is not None:
            if is_preprinted:
                logs = logs.filter(is_preprinted=True)

            if not is_preprinted:
                logs = logs.filter(is_preprinted=False)

        return logs

    @staticmethod
    def colourman_performance(start_date=None, end_date=None):
        qs = Colourman.objects.all()
        if start_date:
            qs = qs.filter(unacceptable__date__gte=start_date)
        if end_date:
            qs = qs.filter(unacceptable__date__lte=end_date)

        return qs.annotate(
            total_points=Sum('unacceptable__points'),
            total_fails=Count('unacceptable')
        ).order_by('-total_points')

    @staticmethod
    def job_history(job_code: str):
        return PrintingLog.objects.filter(job__job_code=job_code).select_related('colourman', 'label', 'job')

    @staticmethod
    def unacceptable_incidents(start_date=None, end_date=None):
        incidents = Unacceptable.objects.all().select_related('colourman')
        if start_date:
            incidents = incidents.filter(date__gte=start_date)
        if end_date:
            incidents = incidents.filter(date__lte=end_date)
        return incidents.order_by('-date')


    @staticmethod
    def total_labels_printed_by_colourman(start_date=None, end_date=None):
        qs = PrintingLog.objects.all().select_related('colourman').distinct('colourman')
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        return qs