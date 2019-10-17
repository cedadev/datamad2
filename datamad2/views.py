from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedGrant, Grant
from .forms import UpdateClaim


@login_required
def grant_detail(request, pk):
    grant_detail = get_object_or_404(ImportedGrant, pk=pk)
    return render(request, 'datamad2/grant_detail.html', {'grant_detail': grant_detail})


def grant_list(request):
    grants = Grant.objects.all()
    return render(request, 'datamad2/grant_list.html', {'grants': grants})

@login_required
def claim(request, pk):
    grant_detail = get_object_or_404(ImportedGrant, pk=pk)
    grant = get_object_or_404(Grant, pk=pk)
    user = request.user
    grant_detail.claim_status = "Claimed"
    grant.assigned_data_centre = user.data_centre
    grant_detail.save()
    grant.save()
    return redirect('grant_list')

@login_required
def unclaim(request, pk):
    grant_detail = get_object_or_404(ImportedGrant, pk=pk)
    grant = get_object_or_404(Grant, pk=pk)
    grant_detail.claim_status = None
    grant.assigned_data_centre = "Unassigned"
    grant_detail.save()
    grant.save()
    return redirect('grant_list')

@login_required
def change_claim(request, pk):
    change_claim = get_object_or_404(Grant, pk=pk)
    form = UpdateClaim(instance=change_claim)
    return render(request, 'datamad2/change_claim.html', {'change_claim': change_claim})

@login_required
def my_account(request):
    return render(request, 'registration/my_account.html', {'my_account': my_account})