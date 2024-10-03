from rest_framework import serializers
from comments.models import Comment
from users.models import CustomUser
from users.utils import get_default_user  # Import the get_default_user function

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user = validated_data.get('user', None)
        if not user:
            default_user_id = get_default_user()
            if default_user_id:
                user = CustomUser.objects.get(pk=default_user_id)
            validated_data['user'] = user
        return super().create(validated_data)
