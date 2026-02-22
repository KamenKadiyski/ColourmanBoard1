from django.urls import path

from reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('<slug:report_slug>/', views.report_view,name='report_view')
]
