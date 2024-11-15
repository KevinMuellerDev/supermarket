from django.contrib import admin
from django.urls import path, include
from .views import MarketsView, MarketDetail, MarketSellerListView, sellers_view, SellerViewSet, ProductViewSet, product_single_view, seller_single_view

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'sellers', SellerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketDetail.as_view(), name='market-detail'),
    path('market/<int:pk>/sellers/', MarketSellerListView.as_view()),


]
