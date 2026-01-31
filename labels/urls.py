from django.urls import path, include

from labels.views import *

app_name = 'labels'


label_urls = [
    path('', labels_index, name='labels_index'),
    path('label_list/', labels_list, name='labels_list'),
    path('sizes/',manage_sizes_view,name='manage_sizes'),
    path('label_types/',manage_label_types_view,name='manage_label_types'),
    path('add_label/',add_label_view,name='add_label'),
    path('<int:pk>/', include([
        path('', label_details, name='label_details'),
        path('edit/',edit_label_view,name='edit_label'),
        path('delete/',delete_label_view,name='delete_label'),
    ])),
]
urlpatterns = [
    path('', index, name='index'),
    path('labels/', include(label_urls))
]

