from django.contrib import admin
from .models import Profile,HouseUnit, Contract,Transaction
from .models import TechnicianReport
from django.utils.html import mark_safe

admin.site.register(Profile)

class HouseUnitAdmin(admin.ModelAdmin):
    list_display = ('owner', 'description', 'location')  # Customize as needed
    list_filter = ('location',)  # Example of adding a filter
    search_fields = ('description', 'owner__username')  # Example of adding search capability

admin.site.register(HouseUnit, HouseUnitAdmin)

class ContractAdmin(admin.ModelAdmin):
    list_display = ('house_unit', 'uploaded_by', 'upload_date', 'contract_image')

    def contract_image(self, obj):
        if obj.contract_file:
            return mark_safe(f'<img src="{obj.contract_file.url}" width="100" />')
        return "No image uploaded."
    contract_image.short_description = 'Contract Image'

admin.site.register(Contract, ContractAdmin)

@admin.register(TechnicianReport)
class TechnicianReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'technician', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'technician__username']

    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'house_unit', 'amount', 'transaction_date', 'processed', 'verified_by')
    list_filter = ('processed', 'transaction_date')
    search_fields = ('user__username', 'house_unit__description')
    actions = ['delete_selected']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Optionally, customize the queryset here, e.g., based on user permissions
        return qs

    def delete_selected(self, request, queryset):
        # Custom action to handle deletion, if necessary
        queryset.delete()
    delete_selected.short_description = "Delete selected transactions"