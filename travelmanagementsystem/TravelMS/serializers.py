from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import (
    Post,
    Tag,
    User,
    Category,
    ActionPost,
    CommentPost,
    CommentTour,
    Rating,
    Tour,
    PostView
)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.save()

        return user

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "password", "email", "avatar", "date_joined"]
        extra_kwargs = {
            'password': {'write_only': 'True'}
        }


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class PostSerializer(ModelSerializer):
    image = SerializerMethodField()
    tags = TagSerializer(many=True)

    def get_image(self, post):
        request = self.context["request"]

        name = post.image.name
        if name.startswith('/static'):
            path = '/%s' % name
        else:
            path = '/static/%s' % name
        return request.build_absolute_uri(path)


    class Meta:
        model = Post
        fields = ["id", "title", "content", "image", "active", "category", "user", "tags"]

class PostViewSerializer(ModelSerializer):
    class Meta:
        model = PostView
        fields = ["post", "views"]

class TourSerializer(ModelSerializer):
    image = SerializerMethodField()

    def get_image(self, tour):

        request = self.context["request"]

        name = tour.image.name
        if name.startswith('/static'):
            path = '/%s' % name
        else:
            path = '/static/%s' % name

        return request.build_absolute_uri(path)

    class Meta:
        model = Tour
        fields = ["id", "name", "tour_type", "image", "tour_days",
                "tour_nights", "adults_price", "children_price", "created_date",
                "updated_date", "start_date", "end_date", "introduction", "service", "note", "active"]

class ActionPostSerializer(ModelSerializer):
    class Meta:
        model = ActionPost
        fields = ["id", "type", "created_date"]

class CommentPostSerializer(ModelSerializer):
    class Meta:
        model = CommentPost
        fields = ["id", "content", "created_date", "updated_date"]

class CommentTourSerializer(ModelSerializer):
    class Meta:
        model = CommentTour
        fields = ["id", "content", "created_date", "updated_date"]


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "rate", "created_date"]
