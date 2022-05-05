from django.contrib import admin
from .models import Account, Client_Transaction
from django.contrib.auth.models import Group
import csv
from django.http import HttpResponse
from .forms import CsvImportForm, ClientTransactionForm
from django.urls import path
from django.shortcuts import redirect, render
from import_export.admin import ImportExportActionModelAdmin

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"

class ClientTransactionAdmin(ExportCsvMixin, admin.ModelAdmin):
    list_display = ['first_name','amount',
                    'transaction_type', 'available_balance', 'minimum_balance', 'account',]
    list_filter = ['account__bank_name']
    list_per_page = 10
    list_display_links = ['amount']
    list_select_related =['transaction_type','available_balance']
    search_fields = ('account__user__first_name',)
    # autocomplete_fields=['account']
    ordering=['-available_balance']
    radio_fields={"account": admin.VERTICAL}

    fieldsets = (
        (None, {
            'fields': ('amount', 'transaction_type', 'available_balance',)
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('account',),
        }),
    )
    # fields=(('amount','transaction_type'),'available_balance')

    def first_name(self, obj):
        return obj.account.user.first_name

    def minimum_balance(self, obj):
        return obj.available_balance >= 10000

    minimum_balance.boolean = True


class InlineClientTransaction(admin.StackedInline):
    model = Client_Transaction
    extra = 2


class AccountAdmin(admin.ModelAdmin):
    list_display = [
        field.name for field in Account._meta.fields if field.name != "id"]


admin.site.register(Account, AccountAdmin)
admin.site.register(Client_Transaction, ClientTransactionAdmin)
admin.site.unregister(Group)

# form=ClientTransactionForm

# inlines =[InlineClientTransaction]

# admin.site.site_header='Vipul Admin'
# admin.site.site_title="Vipul Admin Portal"
# admin.site.index_title='welcome to vipul shopping site'


# class BankingAdminSite(AdminSite):
#    site_header='Vipul Admin'
#    site_title="Vipul Admin Portal"
#    index_title='welcome to vipul shopping site'

# bank_admin_site = BankingAdminSite(name='bank_admin')

# bank_admin_site.register(Account)
# bank_admin_site.register(Client_Transaction)

