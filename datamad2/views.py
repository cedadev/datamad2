from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ImportedGrant, Grant, Document, User, DataCentre, JIRAIssueType, DocumentTemplate, DataProduct
from datamad2.models.data_management_plans import DataFormat, PreservationPlan
from django.http import HttpResponse, FileResponse
from .create_issue import make_issue
from django.urls import reverse, reverse_lazy
from haystack.generic_views import FacetedSearchView
from datamad2.forms import DatamadFacetedSearchForm, UpdateClaimForm, GrantInfoForm, \
    DocumentForm, MultipleDocumentUploadForm, FacetPreferencesForm, \
    DatacentreForm, DatacentreIssueTypeForm, UserForm, DocumentTemplateForm, DocumentGenerationForm
from datamad2.forms.data_product import DigitalDataProductForm, ModelSourceDataProductForm, PhysicalDataProductForm, HardcopyDataProductForm, ThirdPartyDataProductForm, PreservationPlanForm, DataFormatForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.exceptions import ValidationError, ImproperlyConfigured
import re
from django.core.exceptions import ObjectDoesNotExist
from datamad2.tables import GrantTable, DigitalDataProductTable, ModelSourceDataProductTable, PhysicalDataProductTable, HardcopyDataProductTable, ThirdPartyDataProductTable, DataFormatTable, PreservationPlanTable
from jira_oauth.decorators import jira_access_token_required
from django.conf import settings
from django.views.generic.edit import FormView, UpdateView, CreateView
from django.views.generic import TemplateView, ListView
from datamad2.utils import generate_document_from_template
import os
from django_tables2.views import SingleTableView

DOCUMENT_NAMING_PATTERN = re.compile("^(?P<grant_ref>\w*_\w*_\d*)_(?P<doc_type>\w*)(?P<extension>\.\w*)$")

DATAPRODUCT_FORM_CLASS_MAP = {
    'digital': DigitalDataProductForm,
    'model_source': ModelSourceDataProductForm,
    'physical': PhysicalDataProductForm,
    'hardcopy': HardcopyDataProductForm,
    'third_party': ThirdPartyDataProductForm
}

DATAPRODUCT_TABLE_CLASS_MAP = {
    'digital': DigitalDataProductTable,
    'model_source': ModelSourceDataProductTable,
    'physical': PhysicalDataProductTable,
    'hardcopy': HardcopyDataProductTable,
    'third_party': ThirdPartyDataProductTable
}


class FormatError(Exception):
    pass


class UpdateOrCreateMixin:
    def get_object(self, queryset=None):
        """
        Overwrite the get_object method so this view behaves as an update or create view.
        If the object doesn't exist, it will render a blank form so you can create one.
        """

        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        # # If none of those are defined, it's an error.
        # if pk is None and slug is None:
        #     raise AttributeError(
        #         "Generic detail view %s must be called with either an object "
        #         "pk or a slug in the URLconf." % self.__class__.__name__
        #     )

        try:
            # Get the single item from the filtered queryset
            return queryset.get()

        except queryset.model.DoesNotExist:
            return None


class DatacentreAdminTestMixin(UserPassesTestMixin):
    """
    Checks if the user is an admin
    """

    def test_func(self):
        return self.request.user.is_admin


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
                    m = DOCUMENT_NAMING_PATTERN.match(name)
                    if not m:
                        raise FormatError(f"File name {name} is not formatted correctly")

                    grant_ref = m.group('grant_ref').replace('_', '/')

                    file_type = m.group('doc_type').lower()
                    if file_type != 'dmp':
                        file_type = 'support'

                    document = Document(upload=f)

                    try:
                        document.grant = Grant.objects.get(grant_ref=grant_ref)
                    except ObjectDoesNotExist:
                        raise FormatError(f"Grant {grant_ref} does not exist")
                    document.type = file_type
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
    grant = get_object_or_404(Grant, pk=pk)
    imported_grant = grant.importedgrant

    docs = imported_grant.grant.document_set.filter(type='support')
    dmp_docs = imported_grant.grant.document_set.filter(type='dmp')

    if imported_grant.parent_grant:
        parent_docs = imported_grant.parent_grant.document_set.filter(type='support')
        parent_dmps = imported_grant.parent_grant.document_set.filter(type='dmp')

    else:
        parent_docs = Document.objects.none()
        parent_dmps = Document.objects.none()

    return render(request, 'datamad2/grant_detail.html', {
        'imported_grant': imported_grant,
        'supporting_docs': docs | parent_docs,
        'dmp_docs': dmp_docs | parent_dmps,
    })


class DataProductView(LoginRequiredMixin, TemplateView):
    template_name = 'datamad2/dataproduct_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        grant = get_object_or_404(Grant, pk=kwargs['pk'])
        context['grant'] = grant
        context['data_products'] = {product:table(grant.dataproduct_set.filter(data_product_type=product)) for product,table in DATAPRODUCT_TABLE_CLASS_MAP.items()}
        return context


class DataProductUpdateCreateView(LoginRequiredMixin, UpdateView):
    template_name = 'datamad2/dataproduct_form_view.html'
    model = DataProduct

    def get_initial(self):
        initial = super().get_initial()
        initial['grant_id'] = get_object_or_404(Grant, pk=self.kwargs['pk']).pk
        initial['data_product_type'] = self.kwargs['data_product_type']
        return initial

    def get_success_url(self):
        return reverse('dataproduct_view', kwargs={'pk': self.kwargs['pk']})

    def get_form_class(self):
        """Return the form class to use in this view."""
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )

        form_class = DATAPRODUCT_FORM_CLASS_MAP.get(self.kwargs['data_product_type'])
        return form_class

    def get_object(self, **kwargs):
        """
        This modification means this view behaves as an update or create view.
        If the object doesn't exist, it will create one.
        """
        try:
            return self.model.objects.get(pk=self.kwargs['dp_pk'])
        except (ObjectDoesNotExist, KeyError):
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grant'] = get_object_or_404(Grant, pk=self.kwargs['pk'])
        context['data_product_type'] = self.kwargs['data_product_type']
        return context


@login_required
def delete_dataproduct(request, pk, dp_pk):
    data_product = DataProduct.objects.get(pk=dp_pk)
    data_product.delete()
    return redirect(reverse('dataproduct_view', kwargs={'pk':pk}))


class DocumentGenerationSelectView(LoginRequiredMixin, FormView):
    template_name = 'datamad2/generate_document_from_template.html'
    form_class = DocumentGenerationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['imported_grant'] = get_object_or_404(Grant, pk=self.kwargs['pk']).importedgrant
        return context

    def form_valid(self, form):
        template = form.cleaned_data['document_template']
        grant = Grant.objects.get(pk=self.kwargs['pk'])
        context = {
            'grant': grant
        }

        doc = generate_document_from_template(template, context)

        download_filename = f'{grant.grant_ref.replace("/","_")}_{template.type.upper()}{os.path.splitext(template.template.name)[1]}'

        return FileResponse(open(doc,'rb'), as_attachment=True, filename=download_filename)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['datacentre'] = self.request.user.data_centre
        return kwargs



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
    grant = get_object_or_404(Grant, pk=pk)
    jira_required_fields = ['issuetype', 'jira_project']

    # Make sure the user has a data centre
    if not request.user.data_centre:
        messages.error(request,
                       f'Your account is not attributed to a Datacentre. You need to '
                       f'have a Datacentre before you can perform this action')
        return redirect('grant_detail', pk=pk)

    # Make sure the users datacentre matches the grants primary datacentre
    if not request.user.data_centre == grant.assigned_data_centre:
        messages.error(request,
                       f'The assigned datacentre for this grant does not match your datacentre. '
                       f'You cannot create JIRA issues from this grant if yours is not the assigned datacentre.')
        return redirect('grant_detail', pk=pk)

    # Check for required fields in users datacentre
    for field in jira_required_fields:
        if not getattr(request.user.data_centre, field):
            messages.error(request,
                           f'Not all the required fields: {jira_required_fields} have been populated to allow this operation. '
                           f'Please update {reverse("datacentre", request.user.data_centre.pk)}')
            return redirect('grant_detail', pk=pk)

    # There is no jira URL against this grant
    if not grant.jira_ticket:
        issue = make_issue(request, grant.importedgrant)
        link = issue.permalink()

        # Save the ticket link to the correct grant
        if link:
            grant.jira_ticket = link
            grant.save()

    return redirect('grant_detail', pk=pk)


@login_required
def grant_history(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
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
        'labels',
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
        'dmp_agreed'

    ]
    template_name = 'datamad2/grant_list.html'

    def get_table(self, context):
        return GrantTable(data=[item.object for item in context['page_obj'].object_list], orderable=False)

    def get_queryset(self):
        options = {
            "size": settings.HAYSTACK_FACET_LIMIT,
            "order": {"_key": "asc"}
        }
        qs = super().get_queryset()
        for field in self.facet_fields:
            qs = qs.facet(field, **options)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add the facet fields to define an order of the facets
        context['facet_fields'] = self.facet_fields
        context['table'] = self.get_table(context)
        context['containerfluid'] = True
        return context


@login_required
def claim(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    user = request.user
    if not grant.assigned_data_centre:
        grant.assigned_data_centre = user.data_centre
        grant.save()
    return HttpResponse(status=200)


@login_required
def unclaim(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    if request.user.data_centre == grant.assigned_data_centre:
        grant.assigned_data_centre = None
        grant.save()
    return HttpResponse(status=200)


@login_required
def change_claim(request, pk):
    grant = get_object_or_404(Grant, pk=pk)
    if request.method == 'POST':
        form = UpdateClaimForm(request.POST, instance=grant)
        if form.is_valid():
            form.save()
        return redirect(reverse('grant_detail', kwargs={'pk': pk}))
    else:
        form = UpdateClaimForm(instance=grant)
    return render(request, 'datamad2/change_claim.html', {'change_claim': change_claim, 'form': form})


class MyAccountPreferencesView(LoginRequiredMixin, FormView):
    template_name = 'datamad2/user_account/account_preferences.html'
    form_class = FacetPreferencesForm
    success_url = reverse_lazy('preferences')

    def get_initial(self):
        initial = {}
        prefered_facets = self.request.user.preferences.get('prefered_facets', [])
        for facet in prefered_facets:
            initial[facet] = True
        return initial

    def form_valid(self, form):
        preferences = [field for field, value in form.cleaned_data.items() if value]
        user = User.objects.get(pk=self.request.user.pk)
        user.prefered_facets = ','.join(preferences)
        user.save()

        return super().form_valid(form)


class MyAccountDatacentreView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'datamad2/user_account/account_datacentre.html'
    model = DataCentre
    form_class = DatacentreForm

    def test_func(self):
        return self.request.user.is_admin

    def get_success_url(self):
        return reverse('datacentre')

    def get_object(self, **kwargs):
        """
        Overwrite the get_object method to only display the datacentre object for
        the current logged in user
        :param kwargs:
        :return: The current users datacentre
        """
        return get_object_or_404(self.model, pk=self.request.user.data_centre.pk)


class MyAccountDatacentreIssueTypeView(LoginRequiredMixin, DatacentreAdminTestMixin, UpdateView):
    template_name = 'datamad2/user_account/account_datacentre_issuetype.html'
    model = JIRAIssueType
    form_class = DatacentreIssueTypeForm

    def get_success_url(self):
        return reverse('issue_type')

    def get_object(self, **kwargs):
        """
        Overwrite the get_object method to only display the JIRAIssueType object for
        the current logged in users datacentre. This modification also means this view
        behaves as an update or create view. If the object doesn't exist, it will create
        one.
        """
        try:
            return self.model.objects.get(datacentre=self.request.user.data_centre)
        except ObjectDoesNotExist:
            return None

    def get_initial(self):
        initial = super().get_initial()
        if not self.object:
            initial.update({
                'datacentre': self.request.user.data_centre
            })
        return initial


class MyAccountDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'datamad2/user_account/my_account.html'


class MyAccountNewUserView(LoginRequiredMixin, DatacentreAdminTestMixin, CreateView):
    template_name = 'datamad2/user_account/datacentre_new_users.html'
    model = User
    form_class = UserForm

    def get_success_url(self):
        messages.success(self.request, 'User added successfully')
        return reverse('new_user')

    def get_initial(self):
        initial = super().get_initial()
        if not self.object:
            initial.update({
                'data_centre': self.request.user.data_centre
            })
        return initial


class DocumentTemplateListView(LoginRequiredMixin, DatacentreAdminTestMixin, ListView):
    model = DocumentTemplate
    template_name = 'datamad2/user_account/datacentre_document_template_list.html'


class DocumentTemplateCreateView(LoginRequiredMixin, DatacentreAdminTestMixin, CreateView):
    model = DocumentTemplate
    template_name = 'datamad2/user_account/datacentre_document_template_form.html'
    form_class = DocumentTemplateForm

    def get_success_url(self):
        return reverse('document_template_list')

    def get_initial(self):
        initial = super().get_initial()
        if not self.object:
            initial.update({
                'datacentre': self.request.user.data_centre
            })
        return initial


class DocumentTemplateUpdateView(LoginRequiredMixin, DatacentreAdminTestMixin, UpdateView):
    model = DocumentTemplate
    template_name = 'datamad2/user_account/datacentre_document_template_form.html'
    form_class = DocumentTemplateForm

    def get_success_url(self):
        return reverse('document_template_list')


@login_required
def grantinfo_edit(request, pk):
    grant = get_object_or_404(Grant, pk=pk)

    if request.method == "POST":
        form = GrantInfoForm(request.POST, instance=grant)
        if form.is_valid():
            grantinfo = form.save(commit=False)
            grantinfo.save()
            return redirect(reverse('grant_detail', kwargs={'pk': pk}) + "#editable-info")
    else:
        form = GrantInfoForm(instance=grant)
    return render(request, 'datamad2/grantinfo_edit.html', {'form': form, 'grant': grant})


@login_required
def document_upload(request, pk):
    grant = get_object_or_404(Grant, pk=pk)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            name = str(request.FILES.get('upload'))
            try:
                # Check basic name format
                m = DOCUMENT_NAMING_PATTERN.match(name)
                if not m:
                    raise FormatError(f"File name {name} is not formatted correctly")

                # Check grant ref against grant you are trying to upload against
                grant_ref = (m.group('grant_ref')).replace('_', '/')
                if grant_ref != grant.grant_ref:
                    raise FormatError(f"Grant reference in file {name} does not match the grant you are uploading to.")

                # Extract the file type
                file_type = m.group('doc_type').lower()
                if file_type != 'dmp':
                    file_type = 'support'

                if file_type == 'dmp' and grant.dmp_agreed:
                    raise PermissionError('You are trying to upload a DMP to a grant where the DMP has been marked '
                                          'as final. If you intend to provide an update, you must clear the agreed '
                                          'status for the DMP before trying again.')

                # Create the document object
                document = form.save(commit=False)
                document.grant = grant
                document.type = file_type
                document.save()

                messages.success(request, 'File uploaded successfully')
                return redirect(reverse('grant_detail', kwargs={'pk': pk}))

            except ValidationError as exc:
                messages.error(request, f'The file {name} has already been uploaded ')

            except (FormatError, PermissionError) as exc:
                messages.error(request, f"{exc}")
    else:
        form = DocumentForm(instance=grant)

    return render(request, 'datamad2/document_upload.html', {'form': form, 'grant': grant})


def delete_file(request, pk):
    document = Document.objects.get(pk=pk)
    document.delete_file()
    return redirect(reverse('grant_detail', kwargs={'pk': document.grant.pk}))


class DataFormatListView(LoginRequiredMixin, SingleTableView):
    model = DataFormat
    template_name = 'datamad2/user_account/data_format_list.html'
    table_class = DataFormatTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(datacentre=self.request.user.data_centre)
        return qs


class DataFormatUpdateCreateView(LoginRequiredMixin, UpdateOrCreateMixin, UpdateView):
    model = DataFormat
    template_name = 'datamad2/user_account/data_format_form.html'
    form_class = DataFormatForm
    success_url = reverse_lazy('data_format_list')

    def get_initial(self):
        initial = super().get_initial()
        if not self.object:
            initial.update({
                'datacentre': self.request.user.data_centre
            })
        return initial


class PreservationPlanListView(LoginRequiredMixin, SingleTableView):
    model = PreservationPlan
    template_name = 'datamad2/user_account/preservation_plan_list.html'
    table_class = PreservationPlanTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(datacentre=self.request.user.data_centre)

        return qs


class PreservationPlanUpdateCreateView(LoginRequiredMixin, UpdateOrCreateMixin, UpdateView):
    model = PreservationPlan
    template_name = 'datamad2/user_account/preservation_plan_form.html'
    form_class = PreservationPlanForm
    success_url = reverse_lazy('preservation_plan_list')

    def get_initial(self):
        initial = super().get_initial()
        if not self.object:
            initial.update({
                'datacentre': self.request.user.data_centre
            })
        return initial

