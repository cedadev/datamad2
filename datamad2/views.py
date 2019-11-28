from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedGrant, Grant, User
from .forms import UpdateClaim
from django.db.models import Q
from django.http import HttpResponse


@login_required
def grant_detail(request, pk):
    imported_grant = get_object_or_404(ImportedGrant, pk=pk)
    grant = imported_grant.grant
    if grant.importedgrant_set.count() > 1:
        grant.updated_imported_grant = True
        grant.save()
    else:
        grant.updated_imported_grant = False
        grant.save()
    return render(request, 'datamad2/grant_detail.html', {'imported_grant': imported_grant})


def grant_list(request):
    if request.method == 'GET':
        grants = Grant.objects.all()
        assignee = request.GET.get('datacentre')
        if assignee == 'unassigned':
            grants = grants.filter(assigned_data_centre=None)
        elif assignee:
            grants = grants.filter(Q(assigned_data_centre=assignee) | Q(other_data_centre=assignee))
        return render(request, 'datamad2/grant_list.html', {'grants': grants})


def routing_classification(request):
    if request.method == 'GET':
        grants = Grant.objects.all()
        #imported_grants = ImportedGrant.objects.all()
        classification = request.GET.get('rc')
        if classification == 'none':
            grants = grants.filter(importedgrant__routing_classification=None).distinct()
        elif classification:
            grants = grants.filter(importedgrant__routing_classification=classification).distinct()
        return render(request, 'datamad2/routing_classification.html', {'grants': grants})

@login_required
def grant_history(request, pk):
    imported_grant = get_object_or_404(ImportedGrant, pk=pk)
    grant = imported_grant.grant
    return render(request, 'datamad2/grant_history.html', {'grant': grant})

@login_required
def claim(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    user = request.user
    grant.claim_status = "Claimed"
    grant.assigned_data_centre = user.data_centre
    grant.save()
    return HttpResponse(status=200)


@login_required
def unclaim(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    grant.claim_status = None
    grant.assigned_data_centre = None
    grant.save()
    return redirect('grant_list')


@login_required
def change_claim(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    if request.method == 'POST':
        form = UpdateClaim(request.POST, instance=grant)
        if form.is_valid():
            form.save()
            if form.cleaned_data['assigned_data_centre'] is None:
                grant.claim_status = ""
            else:
                grant.claim_status = "Claimed"
            grant.save()
        return redirect('grant_list')
    else:
        form = UpdateClaim(instance=grant)
    return render(request, 'datamad2/change_claim.html', {'change_claim': change_claim, 'form': form})


@login_required
def my_account(request):
    return render(request, 'registration/my_account.html', {'my_account': my_account})
