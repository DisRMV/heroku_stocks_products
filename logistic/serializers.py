from rest_framework import serializers

from .models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockProduct
        fields = ('product', 'quantity', 'price')


class StockSerializer(serializers.ModelSerializer):

    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = '__all__'

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)

        for pos in positions:
            pos.update([('stock', stock)])
            StockProduct.objects.create(**pos)

        return stock

    def update(self, instance, validated_data):

        positions = validated_data.pop('positions')

        stock = super().update(instance, validated_data)

        for pos in positions:
            data = {'stock': instance, 'product': pos.pop('product')}
            StockProduct.objects.update_or_create(**data, defaults=pos)

        return stock
