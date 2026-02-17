from django.urls import path, include

from colourman.views import ColourmanIndexView, add_colourman_view, search_colourman_and_add_unacceptable_view, \
    ColourmanDetailView

app_name = 'colourman'

urlpatterns = [
    path('', ColourmanIndexView.as_view(), name='index'),
    path('add',add_colourman_view,name='add_colourman'),
    path('<int:pk>/', include([
        path('', ColourmanDetailView.as_view(), name='detail'),
        path('unacceptable/',search_colourman_and_add_unacceptable_view,name='unacceptable'),

    ])),
]
