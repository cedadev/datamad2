from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from datamad2.models import Grant, ImportedGrant


# Create your views here.

def project_list(request):
    user = request.user
    projects = Project.objects.filter(grant__assigned_data_centre=user.data_centre)
    return render(request, 'dmp/project_list.html', {'projects': projects})
