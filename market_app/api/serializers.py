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
    
    #nimmt sich seller aus der many to many beziehung von seller zu market und stellt ihn als weiterführenden link zur singleview dar
    sellers =serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Market
        fields=['id','name','location','description','net_worth','sellers']

        
        
class MarketHyperlinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):
    sellers=None
    
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
                
    class Meta:
        model = Market
        fields=['id','name','location', 'sellers','description','net_worth']


class SellerSerializer(serializers.ModelSerializer):
    markets = serializers.StringRelatedField(many=True, read_only=True)
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(),
        many=True,
        write_only=True,
        source = 'markets'
    )
    # deklaration der serializer methode
    market_count = serializers.SerializerMethodField()
    
    class Meta:
        model=Seller
        fields=['id','name','market_count', 'market_ids','markets','contact_info']
        
    def update(self,instance,validated_data):
        markets = validated_data.pop('markets',None)
        instance = super().update(instance, validated_data)
        if markets is not None:
            instance.markets.set(markets)
        instance.save()
        return instance
    
    # get_ muss vor serializer methodfield stehen, eingegebenes object ist das welches bei aufruf des serializers rein gegeben wird
    def get_market_count(self,obj):
        return obj.markets.count()

#

class SellerListSerializer(SellerSerializer,serializers.HyperlinkedModelSerializer):
    markets=serializers.PrimaryKeyRelatedField(queryset=Market.objects.all(), many=True)
    class Meta:
        model=Seller
        fields=['url','name','market_ids','market_count','contact_info']
        

class ProductSerializer(serializers.ModelSerializer):
    markets = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(), many=True
    )
    sellers = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all(), many=True
    )
    class Meta:
        model=Product
        fields='__all__'
    
    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller_ids = validated_data.pop('sellers')

        # Produkt erstellen
        product = Product.objects.create(**validated_data)

        # Märkte und Verkäufer mit dem Produkt verknüpfen
        product.markets.set(market_ids)
        product.sellers.set(seller_ids)

        return product
    
    def to_representation(self, instance):
        # Standard-Darstellung
        representation = super().to_representation(instance)

        # Märkte und Verkäufer durch ihre repräsentativen Strings ersetzen
        representation['markets'] = [market.name for market in instance.markets.all()]
        representation['sellers'] = [seller.name for seller in instance.sellers.all()]

        return representation

class ProductDetailSerializer(serializers.ModelSerializer):
    markets= serializers.SerializerMethodField()
    sellers=serializers.SerializerMethodField()
    
    class Meta:
        model=Product
        fields=['id','name','description','price','markets','sellers']

    def get_markets(self,obj):
        return [market.name for market in obj.markets.all()]
    
    def get_sellers(self,obj):
        return[seller.name for seller in obj.sellers.all()]
    

class ProductCreateSerializer(serializers.ModelSerializer):
    markets = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(), many=True
    )
    sellers = serializers.PrimaryKeyRelatedField(
        queryset=Seller.objects.all(), many=True
    )
    
    class Meta:
        model=Product
        exclude=[]

    def validate_markets(self, value):
        # Stelle sicher, dass alle Market-IDs existieren
        markets = Market.objects.filter(id__in=[market.id for market in value])
        if len(markets) != len(value):
            raise serializers.ValidationError("One or more Market IDs not found.")
        return value

    def validate_sellers(self, value):
        # Stelle sicher, dass alle Seller-IDs existieren
        sellers = Seller.objects.filter(id__in=[seller.id for seller in value])
        if len(sellers) != len(value):
            raise serializers.ValidationError("One or more Seller IDs not found.")
        return value

    def create(self, validated_data):
        # IDs aus validated_data herausnehmen
        market_ids = validated_data.pop('markets')
        seller_ids = validated_data.pop('sellers')

        # Produkt erstellen
        product = Product.objects.create(**validated_data)

        # Märkte und Verkäufer mit dem Produkt verknüpfen
        product.markets.set(market_ids)
        product.sellers.set(seller_ids)

        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.price = validated_data.get(
            'price', instance.price)

        if 'markets' in validated_data:
            market_ids = validated_data.pop('markets')
            instance.markets.set(market_ids)

        if 'sellers' in validated_data:
            seller_ids = validated_data.pop('sellers')
            instance.sellers.set(seller_ids)

        instance.save()
        return instance
    
    
    

