from django.urls import path, include

from jobs.views import jobs_list, CustomerIndexView, JobDetailView

app_name = 'jobs'
jobs_urls = [
    path('',jobs_list,name='jobs_list'),
    path('customers/',CustomerIndexView.as_view(),name='customer_index'),
    path('<int:pk>/',include([
        path('',JobDetailView.as_view(),name='jobs_detail'),
    ])),
    ]
urlpatterns = [
    path('',include(jobs_urls)),
]
