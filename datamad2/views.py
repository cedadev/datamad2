from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedGrant, Grant
from .forms import UpdateClaim, GrantInfoForm
from django.db.models import Q
from django.http import HttpResponse
from .create_issue import make_issue, set_options, get_link
from django.urls import reverse


@login_required
def grant_detail(request, pk):
    imported_grant = get_object_or_404(ImportedGrant, pk=pk)
    user = request.user
    grant_ref = str(imported_grant.grant_ref).replace('/', '\\u002f')
    if request.method == 'POST' and 'jira-issue' and imported_grant.ticket is False:
        # call function
        set_options(user)
        make_issue(user, imported_grant)
        imported_grant.ticket = True
        imported_grant.save()
        # return user to required page
        return redirect('grant_detail', pk=pk)
    elif imported_grant.ticket is True:
        link = get_link(user, grant_ref)
        if link is None:
            imported_grant.ticket = False
            imported_grant.save()
        return render(request, 'datamad2/grant_detail.html', {'imported_grant': imported_grant, 'link': link})
    else:
        imported_grant.ticket = False
        imported_grant.save()
        return render(request, 'datamad2/grant_detail.html', {'imported_grant': imported_grant})


@login_required
def grant_history(request, pk):
    imported_grant = get_object_or_404(ImportedGrant, pk=pk)
    grant = imported_grant.grant
    return render(request, 'datamad2/grant_history.html', {'grant': grant})


@login_required
def grant_history_detail(request, pk, imported_pk):
    grant = get_object_or_404(Grant, pk=pk)
    imported_grant = get_object_or_404(ImportedGrant, pk=imported_pk)
    return render(request, 'datamad2/grant_detail_history.html', {'grant': grant, 'imported_grant': imported_grant})


@login_required
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
def claim(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    user = request.user
    grant.assigned_data_centre = user.data_centre
    grant.save()
    return HttpResponse(status=200)


@login_required
def unclaim(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    grant.assigned_data_centre = None
    grant.save()
    return HttpResponse(status=200)


@login_required
def change_claim(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    if request.method == 'POST':
        form = UpdateClaim(request.POST, instance=grant)
        if form.is_valid():
            form.save()
        return redirect('grant_list')
    else:
        form = UpdateClaim(instance=grant)
    return render(request, 'datamad2/change_claim.html', {'change_claim': change_claim, 'form': form})


@login_required
def my_account(request):
    return render(request, 'registration/my_account.html', {'my_account': my_account})


@login_required
def grantinfo_edit(request, pk, imported_pk):
    grant = get_object_or_404(Grant, pk=pk)
    imported_grant = get_object_or_404(ImportedGrant, pk=imported_pk)
    if request.method == "POST":
        form = GrantInfoForm(request.POST, instance=grant)
        if form.is_valid():
            grantinfo = form.save(commit=False)
            grantinfo.save()
            return redirect(reverse('grant_detail', kwargs={'pk': imported_pk}) + "#spaced-card")
    else:
        form = GrantInfoForm(instance=grant)
    return render(request, 'datamad2/grantinfo_edit.html', {'form': form, 'grant': grant})
