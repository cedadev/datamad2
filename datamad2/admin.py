from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import ImportedGrant, Grant, User

# Register your models here.

class UserCreationForm(forms.ModelForm):
    #form for creating new users
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'data_centre')

    def clean_password2(self):
    #checks the 2 passwords match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
    #save password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    #form for updating a user
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields= ('email', 'first_name', 'last_name', 'password', 'data_centre', 'is_admin')

    def clean_password(self):
        return self.initial["password"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ( 'first_name', 'last_name', 'email','data_centre', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password', 'data_centre')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'data_centre', 'password1', 'password2')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

class ImportedGrantAdmin(admin.ModelAdmin):

    def __init__(self, *args, **kwargs):
        admin.ModelAdmin.__init__(self, *args, **kwargs)
        self.readonly_fields = [f.name for f in self.model._meta.get_fields()]
        self.readonly_fields.remove("importedgrant")
        self.readonly_fields.remove("grant")
        print(self.readonly_fields)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
admin.site.register(ImportedGrant, ImportedGrantAdmin)

class GrantAdmin(admin.ModelAdmin):
    readonly_fields = ['updated_imported_grant']
    pass

admin.site.register(Grant, GrantAdmin)
