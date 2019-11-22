from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, DataProduct
from .forms import DataProductForm
from django.db.models import Q


# Create your views here.

def project_list(request):
    user = request.user
    projects = Project.objects.filter(Q(grant__assigned_data_centre=user.data_centre) | Q(grant__other_data_centre=user.data_centre))
    return render(request, 'dmp/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'dmp/project_detail.html', {'project': project})

@login_required
def dataproduct_new(request):
    if request.method == 'POST':
        form = DataProductForm(request.POST)
        if form.is_valid():
            dp = form.save(commit=False)
            dp.sciSupContact = request.user
            dp.save()
            return redirect('project_detail', pk=dp.pk)
        else:
            form = DataProductForm()
        return render(request, 'dmp/dataproduct_edit.html', {'form': form})

