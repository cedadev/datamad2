# encoding: utf-8

from django import forms

from datamad2.models import JIRATicket

class UpdateJIRAForm(forms.ModelForm):

    class Meta:
        model = JIRATicket
        fields = ('url',)
