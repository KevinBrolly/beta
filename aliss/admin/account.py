import csv
from django.http import HttpResponse
from django.contrib import admin
from aliss.models import ALISSUser, Organisation


admin.site.site_header = "Aliss Admin"
admin.site.site_title = "Aliss Admin Portal"
admin.site.index_title = "Welcome to Aliss admin Portal"

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names, delimiter=";")
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export selected users"


@admin.register(ALISSUser)
class ALISSUserAdmin(admin.ModelAdmin, ExportCsvMixin):
    search_fields = ['email']
    list_display = ['email', 'name', 'is_editor', 'is_staff', 'last_login']
    list_filter = ('is_editor'),
    actions = ['export_as_csv']
    

