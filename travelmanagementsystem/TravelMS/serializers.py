from rest_framework.serializers import ModelSerializer
from .models import Post, Tag


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

class PostSerializer(ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ["id", "title", "content", "image", "active", "category", "user", "tags"]


