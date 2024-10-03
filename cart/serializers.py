from rest_framework import serializers
from cart.models import Cart, CartDetail
from users.models import CustomUser
from users.utils import get_default_user  # Import the get_default_user function

class CartDetailSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = CartDetail
        fields = ['id', 'product', 'quantity']
        read_only_fields = ['id']

class CartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )
    cart_details = CartDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'total_price', 'delivery_address', 'delivery_date', 'delivery_status', 'cart_details']
        read_only_fields = ['id', 'created_at', 'total_price', 'cart_details']

    def create(self, validated_data):
        user = validated_data.get('user', None)
        if not user:
            default_user_id = get_default_user()
            if default_user_id:
                user = CustomUser.objects.get(pk=default_user_id)
            validated_data['user'] = user
        return super().create(validated_data)
