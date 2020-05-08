import csv
from django.contrib import admin
from django.http import HttpResponse
from django.db import models
from aliss.models import Claim, Organisation



class ExportCsvMixin:

    def export_as_csv(self, request, queryset):
    
        meta = self.model._meta
       
        field = ['organisation', 'organisation_id' ]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(queryset)      
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field])        
        return response
        
        export_as_csv.short_description = "Export claimed Organisation"


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin, ExportCsvMixin):
    
    list_filter = ['status', 'created_on']
    list_display = ['organisation', 'status', 'created_on']
    search_fields = ['organisation__name']
    actions = ['export_as_csv']
