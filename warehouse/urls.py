from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views import ProductViewSet, StockTransactionViewSet, home

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'transactions', StockTransactionViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
