from django.urls import path, include

from colourman.views import ColourmanIndexView

app_name = 'colourman'

urlpatterns = [
    path('', ColourmanIndexView.as_view(), name='index'),
    path('<int:pk>/', include([

    ])),
]
