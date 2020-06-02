from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedGrant, Grant, User, Document
from .forms import UpdateClaim, GrantInfoForm, DocumentForm, MultipleDocumentUploadForm
from django.db.models import Q
from django.http import HttpResponse
from .create_issue import make_issue, set_options, get_link
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic.edit import FormView
import re
from django.core.exceptions import ObjectDoesNotExist


class FormatError(Exception):
    pass


class FileFieldView(FormView):
    form_class = MultipleDocumentUploadForm
    template_name = 'datamad2/multiple_document_upload.html'  # Replace with your template.
    success_url = 'actions'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def multiple_document_upload(request):
    if request.method == 'POST':
        form = MultipleDocumentUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('upload')
        if form.is_valid():
            for f in files:
                name = str(f)

                try:
                    pattern = re.compile("^\w{2}_\w\d{6,7}\w*_\d \w*.\w*$")
                    if not pattern.match(name):
                        raise FormatError(f"File name {name} is not formatted correctly")

                    grant_ref = (name.split(' ')[0]).replace('_', '/')
                    doc_type = name.split(' ')[1].split('.')[0]
                    if doc_type == 'DMP':
                        type = 'dmp'
                    else:
                        type = 'support'
                    document = Document(upload=f)
                    try:
                        document.grant = Grant.objects.get(grant_ref=grant_ref)
                    except ObjectDoesNotExist:
                        raise FormatError(f"Grant {grant_ref} does not exist")
                    document.type = type
                    document.save()
                except ValidationError:
                    messages.error(request, f'File {name} already exists')
                except FormatError as exc:
                    messages.error(request, f"{exc}")
            messages.success(request, 'Upload complete')
    else:
        form = MultipleDocumentUploadForm()
    return render(request, 'datamad2/multiple_document_upload.html', {'form': form})



@login_required
def grant_detail(request, pk):
    imported_grant = get_object_or_404(ImportedGrant, pk=pk)
    ig = ImportedGrant.objects.filter(pk=pk)
    user = request.user
    grant_ref = str(imported_grant.grant_ref).replace('/', '\\u002f')

    docs = imported_grant.grant.document_set.filter(type='support')
    dmp_docs = imported_grant.grant.document_set.filter(type='dmp')

    if imported_grant.parent_grant is not None:
        parent_docs = imported_grant.parent_grant.document_set.filter(type='support')
        parent_dmps = imported_grant.parent_grant.document_set.filter(type='dmp')

    else:
        parent_docs = None
        parent_dmps = None

    if request.method == 'POST' and 'jira-issue':
        # call function
        set_options(user)
        make_issue(user, imported_grant)
        ig.update(ticket=True)
        # return user to required page
        return redirect('grant_detail', pk=pk)
    elif imported_grant.ticket is True:
        link = get_link(user, grant_ref)
        if link is None:
            ig.update(ticket=False)
        return render(request, 'datamad2/grant_detail.html', {'imported_grant': imported_grant,
                                                              'link': link, 'docs': docs, 'dmp_docs': dmp_docs,
                                                              'parent_docs':parent_docs, 'parent_dmps':parent_dmps})
    else:
        return render(request, 'datamad2/grant_detail.html', {'imported_grant': imported_grant,
                                                              'docs': docs, 'dmp_docs': dmp_docs,
                                                              'parent_docs':parent_docs, 'parent_dmps':parent_dmps})


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

        # Get grant objects
        grants = Grant.objects.all()

        # Default the view to serve all unassigned grants
        assignee = request.GET.get('datacentre', 'unassigned')

        if assignee == 'unassigned':
            grants = grants.filter(assigned_data_centre=None)

        # If the user has not asked for all, filter
        elif assignee != 'all':
            grants = grants.filter(Q(assigned_data_centre__name=assignee) | Q(other_data_centre__name=assignee))

        return render(request, 'datamad2/grant_list.html', {'grants': grants, 'assignee': assignee})

def routing_classification(request):
    if request.method == 'GET':
        grants = Grant.objects.all()

        classification = request.GET.get('rc')
        if classification == 'none':
            grants = grants.filter(importedgrant__routing_classification=None).filter(importedgrant__science_area=None).distinct()
        elif classification:
            grants = grants.filter(Q(importedgrant__routing_classification=classification) | Q(science_area__icontains=classification)).distinct()

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


@login_required
def document_upload(request, pk, imported_pk, type):
    grant = get_object_or_404(Grant, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            name = str(request.FILES.get('upload'))
            try:

                pattern = re.compile("^\w{2}_\w\d{6,7}\w*_\d \w*.\w*$")
                if not pattern.match(name):
                    raise FormatError(f"File name {name} is not formatted correctly")

                document = form.save(commit=False)
                document.grant = grant
                grant_ref = (name.split(' ')[0]).replace('_', '/')
                if grant_ref != grant.grant_ref:
                    raise FormatError(f"Grant reference in file {name} does not match the grant you are uploading to.")

                document.type = type
                document.save()
                messages.success(request, 'File uploaded successfully')
                return redirect(reverse('grant_detail', kwargs={'pk': imported_pk}))

            except ValidationError as exc:
                messages.error(request, f'This file {name} has already been uploaded')

            except FormatError as exc:
                messages.error(request, f"{exc}")
    else:
        form = DocumentForm(instance=grant)
    return render(request, 'datamad2/document_upload.html', {'form': form})


def dmp_history(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    return render(request, 'datamad2/dmp_history.html', {'grant': grant})


def actions(request):
    return render(request, 'datamad2/admin_actions.html')


def delete_file(request, pk, imported_pk):
    document = Document.objects.get(pk=pk)
    document.delete_file()
    return redirect(reverse('grant_detail', kwargs={'pk': imported_pk}))