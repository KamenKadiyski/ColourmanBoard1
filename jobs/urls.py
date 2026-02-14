from django.urls import path, include

from jobs.views import jobs_list, CustomerIndexView, JobDetailView, AddCustomerView, AddJobView, UpdateJobView, \
    DeleteJobView, EditCustomerView, rested_jobs_list, DeleteCustomerView

app_name = 'jobs'
jobs_urls = [
    path('',jobs_list,name='jobs_list'),
    path('create/',AddJobView.as_view(),name='create_job'),
    path('rested/',rested_jobs_list,name='rested_jobs_list'),
    path('<int:pk>/',include([
        path('',JobDetailView.as_view(),name='jobs_detail'),
        path('edit/',UpdateJobView.as_view(),name='edit_job'),
        path('delete/',DeleteJobView.as_view(),name='delete_job'),
    ])),
    ]

customer_patterns = [
    path('',CustomerIndexView.as_view(),name='customer_index'),
    path('create/',AddCustomerView.as_view(),name='create_customer'),
    path('<int:pk>/',include([
        path('edit/',EditCustomerView.as_view(),name='edit_customer'),
        path('delete/',DeleteCustomerView.as_view(),name='delete_customer'),
    ])),
]

urlpatterns = [
    path('',include(jobs_urls)),
    path('customers/',include(customer_patterns)),
]
