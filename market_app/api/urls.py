from django.contrib import admin
from django.urls import path
from .views import MarketsView, MarketDetail,sellers_view,product_view,product_single_view,seller_single_view

urlpatterns = [
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/',MarketDetail.as_view(), name='market-detail'),
    path('seller/',sellers_view),
    path('seller/<int:pk>/',seller_single_view, name='seller_single'),
    path('product/',product_view),
    path('product/<int:pk>/',product_single_view)

]