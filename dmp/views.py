from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, DataProduct
from .forms import DataProductForm, ProjectForm
from django.db.models import Q
from django.urls import reverse



def project_list(request):
    user = request.user
    projects = Project.objects.filter(Q(grant__assigned_data_centre=user.data_centre) | Q(grant__other_data_centre=user.data_centre))
    return render(request, 'dmp/project_list.html', {'projects': projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'dmp/project_detail.html', {'project': project})


@login_required
def dataproduct_new(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = DataProductForm(request.POST)
        if form.is_valid():
            dp = form.save(commit=False)
            dp.sciSupContact = request.user
            if not dp.sciSupContact:
                dp.sciSupContact = request.user
            if not dp.project:
                dp.project = project
            dp.save()
            return redirect(reverse('project_detail', kwargs={'pk': dp.project.pk}) + "#spaced-card")
    else:
        form = DataProductForm()
    return render(request, 'dmp/dataproduct_edit.html', {'form': form})


@login_required
def dataproduct_edit(request, pk, project_id):
    project = get_object_or_404(Project, pk=project_id)
    dataproduct = get_object_or_404(DataProduct, pk=pk)
    if request.method == "POST":
        form = DataProductForm(request.POST, instance=dataproduct)
        if form.is_valid():
            dp = form.save(commit=False)
            if not dp.sciSupContact:
                dp.sciSupContact = request.user
            if not dp.project:
                dp.project = project
            dp.save()
            return redirect(reverse('project_detail', kwargs={'pk': dp.project.pk}) + "#spaced-card")
    else:
        form = DataProductForm(instance=dataproduct)
    return render(request, 'dmp/dataproduct_edit.html', {'form': form, 'dataproduct': dataproduct})


@login_required
def dataproduct_delete(request, pk):
    dataproduct = get_object_or_404(DataProduct, pk=pk)
    if request.method == 'POST':
        dataproduct.delete()
        return redirect(reverse('project_detail', kwargs={'pk': dataproduct.project.pk}) + "#spaced-card")
    return render(request, 'dmp/dataproduct_edit.html', {'dataproduct': dataproduct})


def dataproduct_detail(request, pk):
    dataproduct = get_object_or_404(DataProduct, pk=pk)
    return render(request, 'dmp/dataproduct_detail.html', {'dataproduct': dataproduct})


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            p = form.save(commit=False)
            p.primary_dataCentre = request.user.data_centre
            p.save()
            return redirect('project_detail', pk=p.pk)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'dmp/project_edit.html', {'form': form, 'project':project})

