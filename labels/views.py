from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from labels.forms import SearchForm, CreateLabelForm
from labels.models import Label


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    nav_path = 'shared/navigation.html'
    page_title = 'Colourman Dashboard'
    context = {
        'nav_path': nav_path,
        'page_title': page_title
    }
    return render(request,'index.html',context)

def labels_index(request: HttpRequest) -> HttpResponse:
    last_labels = Label.objects.prefetch_related('jobs').order_by('-id')[:3]
    nav_path = 'labels/label_nav.html'
    page_title = 'Labels'
    context = {
        'nav_path': nav_path,
        'page_title': page_title,
        'last_labels': last_labels,
    }
    return render(request,'labels/label_index.html',context)


def labels_list(request: HttpRequest) -> HttpResponse:
    nav_path = 'labels/label_nav.html'
    page_title = 'Label search'
    form = SearchForm(request.GET or None)
    list_of_labels = Label.objects.all().order_by('-id')
    if request.method == 'GET' and form.is_valid():
        label_search = form.cleaned_data['search_term']
        list_of_labels = Label.objects.filter(Q(description__icontains=label_search)
                                              | Q(jobs__job_code__icontains=label_search))
    context = {
        'page_title': page_title,
        'nav_path': nav_path,
        'last_labels': list_of_labels,
        'form': form
    }

    return render(request, 'labels/label_list.html', context)


def label_details(request: HttpRequest, pk: int) -> HttpResponse:
    label = get_object_or_404(Label.objects.prefetch_related('jobs'), pk=pk)
    nav_path = 'shared/detail_nav.html'


    context = {
        'label': label,
        'page_title': f'{label.description}',
        'nav_path': nav_path,
    }
    return render(request, 'labels/details.html', context)
def add_label_view(request: HttpRequest) -> HttpResponse:
    nav_path = 'labels/label_nav.html'
    page_title = 'Add Label'
    form = CreateLabelForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('labels:labels_index')
    context = {'form': form,
               'nav_path': nav_path,
               'page_title': page_title}
    return render(request,'labels/create_label.html',context)



def edit_label_view(request: HttpRequest, pk: int) -> HttpResponse:
    return redirect('labels:labels_index')

def manage_sizes_view(request: HttpRequest, pk: int) -> HttpResponse:
    return redirect('labels:labels_index')
def manage_label_types_view(request: HttpRequest, pk: int) -> HttpResponse:
    return redirect('labels:labels_index')

def delete_label_view(request: HttpRequest, pk: int) -> HttpResponse:
    return redirect('labels:labels_index')

