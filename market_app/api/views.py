from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from .serializers import MarketSerializer, SellerSerializer, ProductDetailSerializer, ProductCreateSerializer, MarketHyperlinkedSerializer
from market_app.models import Market, Seller, Product

# function to get and post data, when fetched all data referred to market is fetched
class MarketsView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs) 


class MarketDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




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
        serializer = SellerSerializer(sellers, many=True, context={'request': request})
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
@api_view(['GET','DELETE','PUT'])
def seller_single_view(request, pk):
    try:
        seller = Seller.objects.get(pk=pk)
    except Seller.DoesNotExist:
        return Response({"detail": "Seller not found."}, status=status.HTTP_404_NOT_FOUND,context={'request': request})

    if request.method == 'GET':
        serializer = SellerSerializer(seller, context={'request':request})
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
    
    
@api_view(['GET','POST'])
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


@api_view(['GET','DELETE','PUT'])
def product_single_view(request, pk):

    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        product = Product.objects.get(pk=pk)
        serializer = ProductCreateSerializer(product, data=request.data, partial=True)
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