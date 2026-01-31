from django.urls import path, include

from labels.views import *

app_name = 'labels'


label_urls = [
    path('', labels_index, name='labels_index'),
    path('label_list/', labels_list, name='labels_list'),
    path('label_types/',manage_label_types_view,name='manage_label_types'),
    path('add_label/',add_label_view,name='add_label'),
    path('<int:pk>/', include([
        path('', label_details, name='label_details'),
        path('edit/',edit_label_view,name='edit_label'),
        path('delete/',delete_label_view,name='delete_label'),
    ])),
]

sizes_urls = [
    path('',sizes_index,name='sizes_index'),
    path('create/',sizes_add_view,name='add_size'),
    path('<int:pk>/',include([
        path('edit/',edit_size_view,name='edit_size'),
        path('delete/',delete_size_view,name='delete_size'),

    ])),

]

types_urls = [
    path('',manage_label_types_view,name='manage_label_types'),
    path('create/',add_type_view,name='add_type'),
    path('<int:pk>/',include([
        path('edit/',edit_type_view,name='edit_type'),
        path('delete/',delete_type_view,name='delete_type'),

    ])),

]


urlpatterns = [
    path('', index, name='index'),
    path('labels/', include(label_urls)),
    path('sizes/', include(sizes_urls)),
    path('types/', include(types_urls)),
]

