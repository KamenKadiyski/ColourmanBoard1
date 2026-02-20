from django.urls import path, include

from colourman.views import ColourmanIndexView, add_colourman_view, search_colourman_and_add_unacceptable_view, \
    ColourmanDetailView, UnacceptableDetailView, DeleteColourmanView, EditColourmanView, add_to_printing_log_view

app_name = 'colourman'

urlpatterns = [
    path('', ColourmanIndexView.as_view(), name='index'),
    path('add',add_colourman_view,name='add_colourman'),
    path('add_to_log',add_to_printing_log_view,name='add_to_log'),
    path('<int:cm_pk>/', include([
        path('', ColourmanDetailView.as_view(), name='detail'),
        path('edit/',EditColourmanView.as_view(), name='edit_colourman'),
        path('delete/',DeleteColourmanView.as_view(), name='delete_colourman'),
        path('unacceptable/',include([
            path('add/',search_colourman_and_add_unacceptable_view,name='unacceptable'),
            path('<int:f_pk>/',UnacceptableDetailView.as_view(),name='fail_details'),
        ])),


    ])),
]
