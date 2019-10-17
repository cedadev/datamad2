from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedGrant, Grant, MyUser

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
    grant_detail.claim_status = "Claimed"
    grant_detail.save()
    return redirect('grant_list')

@login_required
def my_account(request):
    return render(request, 'registration/my_account.html', {'my_account': my_account})