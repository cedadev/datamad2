from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedGrant, Grant
from .forms import UpdateClaim
from django.db.models import Q


@login_required
def grant_detail(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    grant_detail = get_object_or_404(ImportedGrant, pk=pk)
    return render(request, 'datamad2/grant_detail.html', {'grant_detail': grant_detail, 'grant': grant})


def grant_list(request):
    if request.method == 'GET':
        grants = Grant.objects.all()
        assignee = request.GET.get('datacentre')
        if assignee == 'unassigned':
            grants = grants.filter(assigned_data_centre=None)
        elif assignee:
            grants = grants.filter(Q(assigned_data_centre=assignee) | Q(other_data_centre=assignee))
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
    grant.assigned_data_centre = None
    grant_detail.save()
    grant.save()
    return redirect('grant_list')


@login_required
def change_claim(request, pk):
    change_claim = get_object_or_404(Grant, pk=pk)
    grant_detail = get_object_or_404(ImportedGrant, pk=pk)
    if request.method == 'POST':
        form = UpdateClaim(request.POST, instance=change_claim)
        if form.is_valid():
            form.save()
            if form.cleaned_data['assigned_data_centre'] is None:
                grant_detail.claim_status = ""
            else:
                grant_detail.claim_status = "Claimed"
            grant_detail.save()
        return redirect('grant_list')
    else:
        form = UpdateClaim(instance=change_claim)
    return render(request, 'datamad2/change_claim.html', {'change_claim': change_claim, 'form': form})


@login_required
def my_account(request):
    return render(request, 'registration/my_account.html', {'my_account': my_account})
