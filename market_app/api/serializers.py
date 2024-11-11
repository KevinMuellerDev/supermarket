from rest_framework import serializers, status
from market_app.models import Market, Seller, Product


def validate_noX(value):
    errors = []
    if 'X' in value:
        errors.append('No X in location')
    if 'Y' in value:
        errors.append('No Y in location')
    if errors:
        raise serializers.ValidationError(errors)
    return value


class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)
    
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(),
        many=True,
        write_only=True,
        source = 'markets'
    )
    class Meta:
        model=Seller
        fields='__all__'
        
    def update(self,instance,validated_data):
        instance = super().update(instance, validated_data)
        if 'markets' in validated_data:
            market_ids = validated_data.pop('markets')
            markets = Market.objects.filter(id__in=market_ids)
            instance.markets.set(markets)
        instance.save()
        return instance


class ProductDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    markets = serializers.StringRelatedField(many=True)
    sellers = serializers.StringRelatedField(many=True)


class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    markets = serializers.ListField(
        child=serializers.IntegerField(), write_only=True)
    sellers = serializers.ListField(
        child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError(
                "One or more Marketids not found")
        return value

    def validate_sellers(self, value):
        sellers = Seller.objects.filter(id__in=value)
        if len(sellers) != len(value):
            raise serializers.ValidationError(
                "One or more Sellerids not found")
        return value

    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller_ids = validated_data.pop('sellers')
        product = Product.objects.create(**validated_data)
        markets = Market.objects.filter(id__in=market_ids)
        product.markets.set(markets)
        sellers = Seller.objects.filter(id__in=seller_ids)
        product.sellers.set(sellers)
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.price = validated_data.get(
            'price', instance.price)

        if 'markets' in validated_data:
            market_ids = validated_data.pop('markets')
            markets = Market.objects.filter(id__in=market_ids)
            instance.markets.set(markets)

        if 'sellers' in validated_data:
            seller_ids = validated_data.pop('sellers')
            sellers = Seller.objects.filter(id__in=seller_ids)
            instance.sellers.set(sellers)

        instance.save()
        return instance
    
    
