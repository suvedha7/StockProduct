from django.contrib import admin
from .models import Product, StockTransaction, TransactionDetail

class TransactionDetailInline(admin.TabularInline):
    model = TransactionDetail
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'current_stock', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    list_display = ('reference_no', 'transaction_type', 'transaction_date', 'created_at')
    list_filter = ('transaction_type', 'transaction_date')
    search_fields = ('reference_no', 'notes')
    inlines = [TransactionDetailInline]
    ordering = ('-transaction_date',)

@admin.register(TransactionDetail)
class TransactionDetailAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'product', 'quantity')
    list_filter = ('transaction__transaction_type', 'product')
    search_fields = ('transaction__reference_no', 'product__name')
    ordering = ('-transaction__transaction_date',)
