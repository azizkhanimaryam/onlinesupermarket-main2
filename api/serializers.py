from rest_framework import serializers
from cart.models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'  # Use '__all__' to include all fields
