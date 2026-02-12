from django.urls import path, include

from jobs.views import jobs_list, CustomerIndexView, JobDetailView, AddCustomerView, AddJobView

app_name = 'jobs'
jobs_urls = [
    path('',jobs_list,name='jobs_list'),
    path('create/',AddJobView.as_view(),name='create_job'),
    path('<int:pk>/',include([
        path('',JobDetailView.as_view(),name='jobs_detail'),
    ])),
    ]

customer_patterns = [
    path('',CustomerIndexView.as_view(),name='customer_index'),
    path('create/',AddCustomerView.as_view(),name='create_customer'),
    #path('<int:pk>/',CustomerIndexView.as_view(),name='update_customer'),
]

urlpatterns = [
    path('',include(jobs_urls)),
    path('customers/',include(customer_patterns)),
]
