from django.db.models import Sum, Count, Q

import labels.models
from colourman.models import PrintingLog, Colourman, Unacceptable
from labels.models import Label
from jobs.models import Job

class ReportLibrary:
    @staticmethod
    def label_usage_log(label_id: int, start_date=None, end_date=None,):
        if label_id:
            logs = PrintingLog.objects.filter(label_id=label_id)
        else:
            logs = PrintingLog.objects.all()
        if start_date:
            logs = logs.filter(usage_date__gte=start_date)
        if end_date:
            logs = logs.filter(usage_date__lte=end_date)


        total_sum = logs.aggregate(total_sum=Sum('amount'))['total_sum'] or 0
        top_colourmen = logs.values('colourman__name').annotate(total_per_employee=Sum('amount')).order_by('-total_per_employee')[:3]

        return {
            'logs': logs,
            'total_sum': total_sum,
            'top_colourmen': top_colourmen
        }

    @staticmethod
    def colourman_performance(start_date=None, end_date=None):
        date_filter = Q()
        if start_date:
            date_filter &= Q(unacceptable__created_at__gte=start_date)
        if end_date:
            date_filter &= Q(unacceptable__created_at__lte=end_date)

        return Colourman.objects.annotate(
            total_points=Sum('unacceptable__points', filter=date_filter),
            total_fails=Count('unacceptable', filter=date_filter)
        ).filter(total_fails__gt=0).order_by('-total_points')

    @staticmethod
    def job_history(job_code: str):
        return PrintingLog.objects.filter(code__job_code=job_code).select_related('colourman', 'label', 'code')

    @staticmethod
    def unacceptable_incidents(start_date=None, end_date=None):
        incidents = Unacceptable.objects.all().select_related('colourman')
        if start_date:
            incidents = incidents.filter(created_at__gte=start_date)
        if end_date:
            incidents = incidents.filter(created_at__lte=end_date)
        return incidents.order_by('-created_at')


    @staticmethod
    def total_labels_printed_by_colourman(start_date=None, end_date=None):
        qs = PrintingLog.objects.all().select_related('colourman').distinct('colourman')
        if start_date:
            qs = qs.filter(date__gte=start_date)
        if end_date:
            qs = qs.filter(date__lte=end_date)
        return qs