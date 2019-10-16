from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedGrant, Grant
from django.http import HttpResponse
from django.contrib import messages


def grant_detail(request, pk):
    grant_detail = get_object_or_404(ImportedGrant, pk=pk)
    return render(request, 'datamad2/grant_detail.html', {'grant_detail': grant_detail})


def grant_list(request):
    grants = Grant.objects.all()
    return render(request, 'datamad2/grant_list.html', {'grants': grants})

@login_required
def claim(request, pk):
    grant_detail = get_object_or_404(ImportedGrant, pk=pk)
    grants = get_object_or_404()
    grant_detail.claim_status = "Claimed"
    grant_detail.save()
    return redirect('grant_list')
