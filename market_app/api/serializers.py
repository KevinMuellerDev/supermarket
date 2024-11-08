from rest_framework import serializers, status
from market_app.models import Market, Seller


def validate_noX(value):
    errors = []
    if 'X' in value:
        errors.append('No X in location')
    if 'Y' in value:
        errors.append('No Y in location')
    if errors:
        raise serializers.ValidationError(errors)
    return value


class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, validators=[validate_noX])
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)

    def create(self, validated_data):
        return Market.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.net_worth = validated_data.get(
            'net_worth', instance.net_worth)
        instance.save()
        return instance


class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField(max_length=255)
    markets = MarketSerializer(read_only=True, many=True)


class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField(max_length=255)
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError("One or more Marketids not found")
        return value
    
    def create(self, validated_data):
        market_ids=validated_data.pop('markets')
        seller=Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id__in=market_ids)
        seller.markets.set(markets)
        return seller

