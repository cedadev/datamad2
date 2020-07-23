from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedGrant, Grant, Document
from .forms import UpdateClaim, GrantInfoForm, DocumentForm, MultipleDocumentUploadForm
from django.http import HttpResponse
from .create_issue import make_issue
from django.urls import reverse
from haystack.generic_views import FacetedSearchView
from datamad2.forms import DatamadFacetedSearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic.edit import FormView
import re
from django.core.exceptions import ObjectDoesNotExist
from datamad2.tables import GrantTable
from jira_oauth.decorators import jira_access_token_required


class FormatError(Exception):
    pass


class FileFieldView(LoginRequiredMixin, FormView):
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
                    pattern = re.compile("^\w*_\w*_\d* \w*.\w*$")
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
                    messages.error(request, f'The file {name} has already been uploaded')
                except FormatError as exc:
                    messages.error(request, f"{exc}")
            messages.success(request, 'Upload complete')
    else:
        form = MultipleDocumentUploadForm()
    return render(request, 'datamad2/multiple_document_upload.html', {'form': form})


@login_required
def grant_detail(request, pk):
    imported_grant = get_object_or_404(ImportedGrant, pk=pk)

    docs = imported_grant.grant.document_set.filter(type='support')
    dmp_docs = imported_grant.grant.document_set.filter(type='dmp')

    if imported_grant.parent_grant:
        parent_docs = imported_grant.parent_grant.document_set.filter(type='support')
        parent_dmps = imported_grant.parent_grant.document_set.filter(type='dmp')

    else:
        parent_docs = None
        parent_dmps = None

    return render(request, 'datamad2/grant_detail.html', {'imported_grant': imported_grant,
                                                              'docs': docs, 'dmp_docs': dmp_docs,
                                                              'parent_docs':parent_docs, 'parent_dmps':parent_dmps})


@login_required
@jira_access_token_required
def push_to_jira(request, pk):
    """
    Create a JIRA ticket from a grant.
    Once the ticket is created, save a link to the ticket with the grant for easy retrieval
    :param request:
    :param pk:
    :return:
    """
    imported_grant = get_object_or_404(ImportedGrant, pk=pk)

    # There is no jira URL against this grant
    if not imported_grant.grant.jira_ticket:
        issue = make_issue(request, imported_grant)
        link = issue.permalink()

        # Save the ticket link to the correct grant
        if link:
            grant = Grant.objects.get(pk=imported_grant.grant.pk)
            grant.jira_ticket=link
            grant.save()

    return redirect('grant_detail', pk=pk)

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


class FacetedGrantListView(LoginRequiredMixin, FacetedSearchView):
    form_class = DatamadFacetedSearchForm
    facet_fields = [
        'assigned_datacentre',
        'routing_classification',
        'other_datacentre',
        'secondary_classification',
        'grant_status',
        'grant_type',
        'scheme',
        'call',
        'facility',
        'lead',
        'ncas',
        'nceo',

    ]
    template_name = 'datamad2/grant_list.html'

    def get_table(self, context):
        return GrantTable(data=[item.object for item in context['page_obj'].object_list], orderable=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the facet fields to define an order of the facets
        context['facet_fields'] = self.facet_fields
        context['table'] = self.get_table(context)
        return context


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

                pattern = re.compile("^\w*_\w*_\d* \w*.\w*$")
                if not pattern.match(name):
                    raise FormatError(f"File name {name} is not formatted correctly")

                document = form.save(commit=False)
                document.grant = grant
                grant_ref = (name.split(' ')[0]).replace('_', '/')
                if grant_ref != grant.grant_ref:
                    raise FormatError(f"Grant reference in file {name} does not match the grant you are uploading to.")

                document.type = type

                file_type = name.split('.')[0][-3:]
                if type == 'dmp':
                    if file_type != 'DMP':
                        raise FormatError(
                            f"Document type in file {name} is not DMP.")

                else:
                    if file_type == 'DMP':
                        raise FormatError(
                            f"Document type in file {name} is DMP and belongs in the DMP document section.")

                document.save()
                messages.success(request, 'File uploaded successfully')
                return redirect(reverse('grant_detail', kwargs={'pk': imported_pk}))

            except ValidationError as exc:
                messages.error(request, f'The file {name} has already been uploaded')

            except FormatError as exc:
                messages.error(request, f"{exc}")
    else:
        form = DocumentForm(instance=grant)
    return render(request, 'datamad2/document_upload.html', {'form': form})


def delete_file(request, pk, imported_pk):
    document = Document.objects.get(pk=pk)
    document.delete_file()
    return redirect(reverse('grant_detail', kwargs={'pk': imported_pk}))

