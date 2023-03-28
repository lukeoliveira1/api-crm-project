from django.contrib import admin
from crm.models import Product, Sale, Company

import locale

# Set the locale to Brazil (Portuguese)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') 

# Register your models here.
class ListProduct(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'photo', 'quantity', 'price_formatted')
    list_display_links = ('id','name')
    search_fields = ('name', 'description')
    list_filter = ('name', 'price')
    list_per_page = 10

    def price_formatted(self, obj):
        # grouping - ensures that the thousands separator is added to the formatted value.
        return locale.currency(obj.price, grouping=True)
    price_formatted.short_description = 'Price'

admin.site.register(Product, ListProduct)

class ListSale(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity_sold', 'sale_date')
    list_display_links = ('id', 'product')
    search_fields = ('product', 'sale_date')
    list_filter = ('sale_date',)
    list_per_page = 10

admin.site.register(Sale, ListSale)

class ListCompany(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'total_revenue_formatted')
    list_display_links = ('id', 'company_name')
    search_fields = ('company_name',)
    list_filter = ('total_revenue',)
    list_per_page = 10

    def total_revenue_formatted(self, obj):
        # grouping - ensures that the thousands separator is added to the formatted value.
        return locale.currency(obj.total_revenue, grouping=True)
    total_revenue_formatted.short_description = 'Total Revenue'

  
admin.site.register(Company, ListCompany)