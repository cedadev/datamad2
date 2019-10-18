from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedGrant, Grant
from .forms import UpdateClaim
from django.db.models import Q


@login_required
def grant_detail(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    grant_detail = get_object_or_404(ImportedGrant, pk=pk)
    return render(request, 'datamad2/grant_detail.html', {'grant_detail': grant_detail, 'grant':grant})


def grant_list(request):
    grants = Grant.objects.all()
    assignee = request.GET.get('data_centre', '')
        # if assignee:
        #     all = grants
        #     unassigned = grants.filter(assigned_data_centre=None)
        #     bodc = grants.filter(Q(assigned_data_centre="BODC")|Q(other_data_centre="BODC"))
        #     ceda = grants.filter(Q(assigned_data_centre="CEDA") | Q(other_data_centre="CEDA"))
        #     eidc = grants.filter(Q(assigned_data_centre="EIDC") | Q(other_data_centre="EIDC"))
        #     ngdc = grants.filter(Q(assigned_data_centre="NGDC") | Q(other_data_centre="NGDC"))
        #     pdc = grants.filter(Q(assigned_data_centre="PDC") | Q(other_data_centre="PDC"))
        #     ads = grants.filter(Q(assigned_data_centre="ADS")|Q(other_data_centre="ADS"))
        #     grants = all | unassigned | bodc | ceda | eidc | ngdc | pdc | ads | grants
    return render(request, 'datamad2/grant_list.html', {'grants': grants, 'filter': assignee})



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
        return redirect('grant_list')
    else:
        form = UpdateClaim(instance=change_claim)
    return render(request, 'datamad2/change_claim.html', {'change_claim': change_claim, 'form': form})


@login_required
def my_account(request):
    return render(request, 'registration/my_account.html', {'my_account': my_account})
