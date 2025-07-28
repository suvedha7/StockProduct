from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from django.shortcuts import render
from .models import Product, StockTransaction, TransactionDetail
from .serializers import ProductSerializer, StockTransactionSerializer

def home(request):
    return render(request, 'inventory/home.html')

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StockTransactionViewSet(viewsets.ModelViewSet):
    queryset = StockTransaction.objects.all().order_by('-transaction_date')
    serializer_class = StockTransactionSerializer

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def stock_summary(self, request):
        products = Product.objects.all()
        data = [{
            'id': product.id,
            'name': product.name,
            'unit': product.unit,
            'current_stock': product.current_stock
        } for product in products]
        return Response(data)
