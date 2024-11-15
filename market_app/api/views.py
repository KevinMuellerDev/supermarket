from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from .serializers import MarketSerializer, SellerSerializer, SellerListSerializer, ProductSerializer,ProductDetailSerializer, ProductCreateSerializer, MarketHyperlinkedSerializer
from market_app.models import Market, Seller, Product

# function to get and post data, when fetched all data referred to market is fetched


class MarketsView(generics.ListCreateAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class MarketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class MarketSellerListView(generics.ListCreateAPIView):
    serializer_class = SellerListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk=pk)
        return market.sellers.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk=pk)
        existing_markets = serializer.validated_data.get('markets', [])
        serializer.save(markets=list(existing_markets))


# @api_view(['GET', 'POST'])
# def markets_view(request):
#     if request.method == 'GET':
#         markets = Market.objects.all()
#         serializer = MarketHyperlinkedSerializer(markets, many=True, context={'request':request}, fields=('id','name','net_worth'))
#         return Response(serializer.data)

#     if request.method == 'POST':
#         serializer = MarketSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# single view to get delete and change data, pk means primary key


# @api_view(['GET', 'DELETE', 'PUT'])
# def market_single_view(request, pk):
#     if request.method == 'GET':
#         market = Market.objects.get(pk=pk)
#         serializer = MarketSerializer(market,context={'request': request})
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         market = Market.objects.get(pk=pk)
#         serializer = MarketSerializer(market, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

#     if request.method == 'DELETE':
#         market = Market.objects.get(pk=pk)
#         serializer = MarketSerializer(market)
#         market.delete()
#         return Response(serializer.data)


@api_view(['GET', 'POST'])
def sellers_view(request):

    if request.method == 'GET':
        sellers = Seller.objects.all()
        serializer = SellerSerializer(
            sellers, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'DELETE', 'PUT'])
def seller_single_view(request, pk):
    try:
        seller = Seller.objects.get(pk=pk)
    except Seller.DoesNotExist:
        return Response({"detail": "Seller not found."}, status=status.HTTP_404_NOT_FOUND, context={'request': request})

    if request.method == 'GET':
        serializer = SellerSerializer(seller, context={'request': request})
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = SellerSerializer(seller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.method == 'DELETE':
        seller.delete()
        return Response("File deleted")


class SellerViewSet(viewsets.ModelViewSet):
    queryset=Seller.objects.all()
    serializer_class = SellerSerializer



class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer






class ProductViewSetOld(viewsets.ViewSet):
    queryset = Product.objects.all()

    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def destroy(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        product.delete()
        return Response("Product ist deleted")






@api_view(['GET', 'POST'])
def product_view(request):
    if request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductDetailSerializer(product, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'DELETE', 'PUT'])
def product_single_view(request, pk):

    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    if request.method == 'PUT':
        product = Product.objects.get(pk=pk)
        serializer = ProductCreateSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.method == 'DELETE':
        product = Product.objects.get(pk=pk)
        serializer = ProductDetailSerializer(product)
        product.delete()
        return Response(serializer.data)
