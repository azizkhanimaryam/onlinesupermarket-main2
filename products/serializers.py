from rest_framework import serializers
from products.models import Category, Product, Stock
from users.models import CustomUser
from users.utils import get_default_user

class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(
        slug_field='email',  # Display the email of the creator
        queryset=CustomUser.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'created_by']
        read_only_fields = ['id']


class StockSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Product.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Stock
        fields = ['id', 'product', 'category', 'quantity']
        read_only_fields = ['id']

    def validate(self, data):
        """Ensure the stock's category matches the product's category."""
        if data['product'].category != data['category']:
            raise serializers.ValidationError("The category of the stock must match the category of the product.")
        return data


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )
    created_by = serializers.SlugRelatedField(
        slug_field='email',
        queryset=CustomUser.objects.all(),
        allow_null=True,
        required=False
    )
    stocks = StockSerializer(many=True, read_only=True)  # Nested serializer for stocks

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'producer', 'description', 'price', 'image', 'availability', 'created_by',
                  'stocks']
        read_only_fields = ['id', 'availability', 'stocks']

    def create(self, validated_data):
        """Override to manage created_by field and set default creator."""
        user = validated_data.get('created_by', None)
        if not user:
            default_user_id = get_default_user()
            if default_user_id:
                user = CustomUser.objects.get(pk=default_user_id)
            validated_data['created_by'] = user

        return super().create(validated_data)
