from django.contrib import messages
from django.db.models import QuerySet, Q, Count, F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from colourman.forms import SearchForm, AddColourmanForm, AddUnacceptableColourmanForm, AddPrintOrUsageOfLabelForm
from colourman.models import Colourman, Unacceptable
from django.urls import reverse, reverse_lazy


# Create your views here.


class ColourmanIndexView(ListView):
    model = Colourman
    template_name = 'colourman/colourman_list.html'
    form = SearchForm
    page_title = 'Colourman list'
    nav_path = 'colourman/colours_nav.html'


    def get_queryset(self) -> QuerySet:
        qs = (super()
              .get_queryset().order_by(F('clock_number').asc())
              .prefetch_related('unacceptable'))
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

def search_colourman_and_add_unacceptable_view(request: HttpRequest, cm_pk:int) -> HttpResponse:

    add_form = AddUnacceptableColourmanForm(request.POST or None)
    colourman = get_object_or_404(Colourman, pk=cm_pk)
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
    pk_url_kwarg = 'cm_pk'
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



class UnacceptableDetailView(UpdateView):
    model = Unacceptable
    fields = '__all__'
    pk_url_kwarg = 'f_pk'
    template_name = 'colourman/fail_detail_update.html'

    def post(self, request, *args, **kwargs):

        if 'edit' in request.POST:
            url = reverse(
                'colourman:fail_details',
                kwargs={
                    'cm_pk': self.kwargs['cm_pk'],
                    'f_pk': self.kwargs['f_pk']
                }
            )
            return redirect(f"{url}?edit=1")


        return super().post(request, *args, **kwargs)


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        editing = self.request.GET.get('edit') == '1'

        if not editing:
            for field in form.fields.values():
                field.disabled = True

        return form


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = 'Unacceptable details'
        nav_path = 'colourman/colours_nav.html'
        context.update({
            'page_title': page_title,
            'nav_path': nav_path,

        })
        return context



    def get_success_url(self):
        return reverse(
            'colourman:fail_details',
            kwargs={
                'cm_pk': self.object.colourman.pk,
                'f_pk': self.object.pk
            }
        )





class DeleteColourmanView(DeleteView):
    model = Colourman
    pk_url_kwarg = 'cm_pk'
    template_name = 'colourman/delete_colourman.html'
    success_url = reverse_lazy('colourman:index')
    page_title = 'Delete Colourman'
    nav_path = 'colourman/colours_nav.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        points = self.object.sum_of_fails_points
        fails_count = self.object.number_of_fails
        context.update({
            'page_title': self.page_title,
            'nav_path': self.nav_path,
            'fails_count': fails_count,
            'points': points,

        })
        return context


class EditColourmanView(UpdateView):
    model = Colourman
    fields = '__all__'
    pk_url_kwarg = 'cm_pk'
    template_name = 'colourman/edit_colourman.html'
    success_url = reverse_lazy('colourman:index')
    page_title = 'Edit Colourman'
    nav_path = 'colourman/colours_nav.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': self.page_title,
            'nav_path': self.nav_path,

        })

        return context


def add_to_printing_log_view(request: HttpRequest) -> HttpResponse:
    form = AddPrintOrUsageOfLabelForm(request.POST or None)
    page_title = 'Add to printing log'
    nav_path = 'colourman/colours_nav.html'
    if request.method == 'POST':
        if 'submit' in request.POST:
            if form.is_valid():
                form.save()
                return redirect('colourman:index')
        else:
            form.is_valid()


    context = {
        'page_title': page_title,
        'nav_path': nav_path,
        'form': form,
    }

    return render(request,'colourman/add_to_log.html',context)






def custom_404(request, exception):
    return render(request, '404.html', status=404)
