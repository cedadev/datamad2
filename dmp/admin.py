from django.contrib import admin
from .models import Project, Programme, DataProduct, Note

admin.site.register(Project)
admin.site.register(Programme)
admin.site.register(DataProduct)
admin.site.register(Note)

