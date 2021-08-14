from rest_framework.serializers import ModelSerializer
from .models import Post, Tag, User



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password", "email", "avatar"]
        extra_kwargs = {
            'password': { 'write_only': 'True' }
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "image", "active", "category", "user", "tags"]


