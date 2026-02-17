from django.contrib import messages
from django.db.models import QuerySet, Q, Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from colourman.forms import SearchForm, AddColourmanForm, AddUnacceptableColourmanForm
from colourman.models import Colourman


# Create your views here.


class ColourmanIndexView(ListView):
    model = Colourman
    template_name = 'colourman/colourman_list.html'
    form = SearchForm
    page_title = 'Colourman list'
    nav_path = 'colourman/colours_nav.html'


    def get_queryset(self) -> QuerySet:
        qs = (super()
              .get_queryset()
              .order_by('-clock_number'))
        if 'search_term' in self.request.GET:
            search_term = self.request.GET['search_term']
            qs = (qs.filter(
                Q(name__icontains=search_term) |
                Q(clock_number__icontains=search_term)
            ))


        return qs.prefetch_related('unacceptable').annotate(fail_count=Count('unacceptable'))
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context.update({
            'nav_path': self.nav_path,
            'page_title': self.page_title,
            'form': self.form,

        })
        return context



def add_colourman_view(request: HttpRequest) -> HttpResponse:
    page_title = 'Add Colourman'
    nav_path = 'colourman/colours_nav.html'
    form = AddColourmanForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('colourman:index')
    context = {
        'form': form,
        'page_title': page_title,
        'nav_path': nav_path,

    }
    return render(request,'colourman/add_colourman.html',context)

def search_colourman_and_add_unacceptable_view(request: HttpRequest, pk:int) -> HttpResponse:

    add_form = AddUnacceptableColourmanForm(request.POST or None)
    colourman = get_object_or_404(Colourman, pk=pk)
    page_title = 'Add unacceptable for colourman'
    nav_path = 'colourman/colours_nav.html'

    if request.method == 'POST' and add_form.is_valid():

        fail = add_form.save(commit=False)
        fail.colourman = colourman
        messages.success(request, 'Unacceptable successfully added!')
        fail.save()
        return redirect('colourman:index')

    context = {

                'add_form': add_form,
                'page_title': page_title,
                'nav_path': nav_path,
                'colourman': colourman,
            }

    return render(request,'colourman/add_unacceptable.html',context)




class ColourmanDetailView(DetailView):
    model = Colourman
    page_title = 'Colourman Detail'
    nav_path = 'colourman/colours_nav.html'
    template_name = 'colourman/colourman_details.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fails_count = self.object.number_of_fails
        fails_list = self.object.list_of_fails
        points = self.object.sum_of_fails_points
        context.update({
            'page_title': self.page_title,
            'nav_path': self.nav_path,
            'fails_count': fails_count,
            'fails_list': fails_list,
            'points_sum': points,



        })
        return context
