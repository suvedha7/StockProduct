from rest_framework import serializers
from .models import Product, StockTransaction, TransactionDetail

class ProductSerializer(serializers.ModelSerializer):
    current_stock = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'unit', 'current_stock', 'created_at', 'updated_at']

class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = ['id', 'product', 'quantity', 'notes']

class StockTransactionSerializer(serializers.ModelSerializer):
    details = TransactionDetailSerializer(many=True, source='transactiondetail_set')

    class Meta:
        model = StockTransaction
        fields = ['id', 'transaction_type', 'transaction_date', 'reference_no', 'notes', 'details', 'created_at']

    def create(self, validated_data):
        details_data = validated_data.pop('transactiondetail_set')
        transaction = StockTransaction.objects.create(**validated_data)
        
        for detail_data in details_data:
            TransactionDetail.objects.create(transaction=transaction, **detail_data)
        
        return transaction