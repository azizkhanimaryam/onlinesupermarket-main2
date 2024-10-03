from rest_framework import serializers
from users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name', 'phone', 'is_active', 'is_staff']
        read_only_fields = ['id', 'is_staff', 'is_active']

    # Optionally, you can define custom validation logic
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        """Override the create method to use the manager's create_user function."""
        return CustomUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Override the update method to handle password changes."""
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance
