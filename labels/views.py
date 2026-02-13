from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from labels.forms import SearchForm, CreateLabelForm, EditLabelForm, DeleteLabelForm, LabelSizeForm, LabelTypeForm
from labels.models import Label, LabelSize, LabelType


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
    link1 = 'labels:edit_label'
    link2 = 'labels:delete_label'
    link3 = 'labels:labels_list'

    context = {
        'label': label,
        'page_title': f'{label.description}',
        'nav_path': nav_path,
        'link1': link1,
        'link2' : link2,
        'link3' : link3,
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
    form = EditLabelForm(request.POST or None, request.FILES or None ,instance=get_object_or_404(Label, pk=pk),)
    page_title = 'Edit Label'
    nav_path = 'labels/label_nav.html'
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('labels:labels_index')
    context = {'form': form,
               'nav_path': nav_path,
               'page_title': page_title
               }
    return render(request, 'labels/edit_label.html', context)


def delete_label_view(request: HttpRequest, pk: int) -> HttpResponse:
    label = get_object_or_404(Label, pk=pk)

    page_title = 'Delete Label'
    nav_path = 'labels/label_nav.html'
    if request.method == 'POST':
        label.delete()
        return redirect('labels:labels_index')

    context = {
        'label': label,

        'page_title': page_title,
        'nav_path': nav_path,
    }
    return render(request,'labels/delete_label.html',context)


def sizes_index(request: HttpRequest) -> HttpResponse:
    last_sizes = LabelSize.objects.all().order_by('-id')
    manage_var = 'labels:add_size'
    nav_pat = 'shared/manage_nav.html'
    page_title = 'Label Sizes'
    context = {
        'manage_var': manage_var,
        'nav_path': nav_pat,
        'page_title': page_title,
        'last_sizes': last_sizes,

    }
    return render(request,'labels/sizes_index.html',context)

def edit_size_view(request: HttpRequest, pk: int) -> HttpResponse:
    size_to_edit = get_object_or_404(LabelSize, pk=pk)
    form = LabelSizeForm(request.POST or None, instance=size_to_edit)
    nav_path = 'shared/manage_nav.html'
    page_title = 'Edit Label Size'
    manage_var = 'labels:add_size'
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('labels:sizes_index')
    context = {'form': form,
               'nav_path': nav_path,
               'page_title': page_title
               , 'manage_var': manage_var
               }
    return render(request,'labels/edit_size.html',context)


def delete_size_view(request: HttpRequest, pk: int) -> HttpResponse:
    size_to_delete = get_object_or_404(LabelSize, pk=pk)
    nav_path = 'shared/manage_nav.html'
    page_title = 'Delete Label Size'
    manage_var = 'labels:add_size'
    if request.method == 'POST':
        size_to_delete.delete()
        return redirect('labels:sizes_index')
    context = {'size': size_to_delete,
               'nav_path': nav_path,
               'page_title': page_title,
               'manage_var': manage_var}
    return render(request,'labels/delete_size.html',context)


def sizes_add_view(request: HttpRequest) -> HttpResponse:
    form = LabelSizeForm(request.POST or None)
    nav_path = 'shared/manage_nav.html'
    page_title = 'Add Label Size'
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('labels:sizes_index')
    context = {'form': form,
               'nav_path': nav_path,
               'page_title': page_title}

    return render(request,'labels/add_size.html',context)


def manage_label_types_view(request: HttpRequest,) -> HttpResponse:
    last_types = LabelType.objects.prefetch_related('sizes').order_by('-id')
    nav_pat = 'labels/types_nav.html'
    page_title = 'Label types'
    context = {
        'nav_path': nav_pat,
        'page_title': page_title,
        'last_types': last_types,
    }
    return render(request, 'labels/type_index.html', context)

def add_type_view(request: HttpRequest) -> HttpResponse:
    nav_path = 'labels/types_nav.html'
    page_title = 'Add Label Type'
    form = LabelTypeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('labels:manage_label_types')
    context = {'form': form,
               'nav_path': nav_path,
               'page_title': page_title

    }
    return render(request,'labels/create_type.html', context)

def edit_type_view(request: HttpRequest, pk: int) -> HttpResponse:
    type_to_edit = get_object_or_404(LabelType, pk=pk)
    form = LabelTypeForm(request.POST or None, instance=type_to_edit)
    nav_path = 'labels/types_nav.html'
    page_title = 'Edit Label Type'
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('labels:manage_label_types')
    context = {'form': form,
               'nav_path': nav_path,
               'page_title': page_title}

    return render(request,'labels/edit_type.html',context)

def delete_type_view(request: HttpRequest, pk: int) -> HttpResponse:
    type_to_delete = get_object_or_404(LabelType, pk=pk)
    nav_path = 'labels/types_nav.html'
    page_title = 'Delete Label Type'
    if request.method == 'POST':
        type_to_delete.delete()
        return redirect('labels:manage_label_types')
    context = {'type': type_to_delete,
               'nav_path': nav_path,
               'page_title': page_title}
    return render(request,'labels/delete_type.html',context)