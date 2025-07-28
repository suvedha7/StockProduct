from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unit = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def current_stock(self):
        total_in = sum(detail.quantity for detail in self.transactiondetail_set.filter(transaction__transaction_type='IN'))
        total_out = sum(detail.quantity for detail in self.transactiondetail_set.filter(transaction__transaction_type='OUT'))
        return total_in - total_out

class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
    ]

    transaction_type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    transaction_date = models.DateTimeField()
    reference_no = models.CharField(max_length=50, unique=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.reference_no} - {self.transaction_type}"

class TransactionDetail(models.Model):
    transaction = models.ForeignKey(StockTransaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.transaction.reference_no} - {self.product.name} - {self.quantity}"

    class Meta:
        verbose_name = 'Transaction Detail'
        verbose_name_plural = 'Transaction Details'
