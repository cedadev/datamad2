from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models.grants import ImportedGrant, Grant
from .models.users import User, DataCentre, Subtask, JIRAIssueType
from .models.document_store import Document
from .models.data_management_plans import *


class UserAdmin(BaseUserAdmin):
    list_display = ( 'first_name', 'last_name', 'email','data_centre', 'is_admin')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password', 'data_centre')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'groups','user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

admin.site.register(User, UserAdmin)


class ImportedGrantAdmin(admin.ModelAdmin):
    search_fields = ['grant_ref', 'title']
    list_display = ('grant_ref', 'title', 'creation_date')

    def __init__(self, *args, **kwargs):
        admin.ModelAdmin.__init__(self, *args, **kwargs)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ImportedGrant, ImportedGrantAdmin)


class GrantAdmin(admin.ModelAdmin):
    readonly_fields = ['updated_imported_grant', 'science_area']
    search_fields = ['grant_ref', 'importedgrant__title']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Grant, GrantAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'grant')

    search_fields = ['title', 'grant__grant_ref']
    autocomplete_fields = ['grant']

admin.site.register(Document, DocumentAdmin)


class DataCentreAdmin(admin.ModelAdmin):
    pass

admin.site.register(DataCentre, DataCentreAdmin)


class SubtaskAdmin(admin.ModelAdmin):
    pass

admin.site.register(Subtask, SubtaskAdmin)


class JIRAIssueTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(JIRAIssueType, JIRAIssueTypeAdmin)


class DocumentTemplateAdmin(admin.ModelAdmin):
    pass
admin.site.register(DocumentTemplate, DocumentTemplateAdmin)


class DataFormatAdmin(admin.ModelAdmin):
    pass
admin.site.register(DataFormat, DataFormatAdmin)


class PreservationPlanAdmin(admin.ModelAdmin):
    pass
admin.site.register(PreservationPlan, PreservationPlanAdmin)


class DataProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(DataProduct, DataProductAdmin)
