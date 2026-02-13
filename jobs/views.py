
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView

import jobs.forms
from jobs.forms import *
from jobs.models import Customer


# Create your views here.


def jobs_list(request: HttpRequest) -> HttpResponse:
    form = JobSearchForm(request.GET or None)
    page_title = 'Job search'
    nav_path = 'jobs/jobs_nav.html'

    jobs = Job.objects.all().prefetch_related('customer','labels__label_types').order_by('-id')
    if request.method == 'GET' and form.is_valid():
        jobs_search = form.cleaned_data['search_term']
        if jobs_search:
            jobs = jobs.filter(
                Q(job_code__icontains=jobs_search) |
                Q(customer__name__icontains=jobs_search) |
                Q(description__icontains=jobs_search)
            )
    context = {
        'nav_path': nav_path,
        'page_title': page_title,
        'jobs': jobs,
        'form': form
    }

    return render(request,'jobs/jobs_index.html',context)
class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    nav_path = 'shared/detail_nav.html'
    page_title = 'Job details'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'nav_path': self.nav_path,
            'page_title': self.page_title,
        })
        return context


    def job(self, request, *args, **kwargs):
        job = self.get_object()

        return super().get(request, *args, **kwargs)


class AddJobView(CreateView):
    model = Job
    fields = '__all__'
    form = AddJobForm
    template_name = 'jobs/add_job.html'
    page_title = 'Add Job'
    nav_path = 'jobs/jobs_nav.html'
    success_url = reverse_lazy('jobs:jobs_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'nav_path': self.nav_path,
            'page_title': self.page_title,

        })
        return context

    def form_valid(self, form):
        job = form.save(commit=False)

        barcode = form.cleaned_data['barcode']
        labels = form.cleaned_data['labels']
        preprinted = labels.filter(label_types__is_preprinted=True).first()

        if preprinted:
            job.barcode = preprinted.bar_code
        else:
            job.barcode = barcode
        job.save()
        form.save_m2m()
        return super().form_valid(form)
            



class CustomerIndexView(ListView, FormView):
    model = Customer
    context_object_name = 'customers'
    template_name = 'jobs/customer_index.html'
    form_class = jobs.forms.CustomerSearchForm
    nav_path = 'jobs/jobs_nav.html'
    page_title = 'Customers list'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'nav_path': self.nav_path,
            'page_title': self.page_title,

        })
        return context

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset().prefetch_related('customers')
        if 'search_term' in self.request.GET:
            qs = qs.filter(name__icontains=self.request.GET['search_term'])


        return qs


class AddCustomerView(CreateView):
    model = Customer
    fields = '__all__'
    template_name = 'jobs/add_customer.html'
    page_title = 'Add Customer'
    nav_path = 'jobs/jobs_nav.html'
    success_url = reverse_lazy('jobs:customer_index')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({

            'page_title': self.page_title,
            'nav_path': self.nav_path,

        })
        return context
