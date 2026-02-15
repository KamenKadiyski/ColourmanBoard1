from django.db.models import QuerySet, Q
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from colourman.forms import SearchForm
from colourman.models import Colourman



# Create your views here.


class ColourmanIndexView(ListView):
    model = Colourman
    template_name = 'colourman/colourman_list.html'
    form = SearchForm
    page_title = 'Colourman list'
    nav_path = 'colourman/colours_nav.html'


    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset().order_by('pk')
        if 'search_term' in self.request.GET:
            search_term = self.request.GET['search_term']
            qs = qs.filter(
                Q(name__icontains=search_term) |
                Q(clock_number__icontains=search_term),

                           )

        return qs