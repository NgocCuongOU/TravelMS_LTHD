from typing import Union

from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, permissions, status, generics
from rest_framework.views import APIView

from .paginator import BasePagination
from django.http import Http404

from django.conf import settings

from .models import (
    Post,
    Tag,
    User,
    Category,
    ActionPost,
    Tour,
    CommentPost,
    CommentTour,
    Rating,
    PostView
)

from .serializers import (
    PostSerializer,
    TagSerializer,
    UserSerializer,
    CategorySerializer,
    ActionPostSerializer,
    TourSerializer,
    RatingSerializer,
    PostViewSerializer,
    CommentPostSerializer,
    CommentTourSerializer,
)

from django.db.models import F


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path="current-user")
    def get_current_user(self, request):
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)

class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    serializer_class = PostSerializer
    pagination_class = BasePagination

    def get_permissions(self):
        if self.action in ['take_action', 'add_comment']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        post = Post.objects.filter(active=True)

        q = self.request.query_params.get('q')
        if q is not None:
            post = post.filter(title__icontains = q)

        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            post = post.filter(category_id = cate_id)

        return post

    # @swagger_auto_schema(
    #     operation_description='Ẩn một bài viết từ phía client',
    #     responses={
    #         status.HTTP_200_OK: PostSerializer()
    #     }
    # )
    # @action(methods=['post'], detail=True, url_path="hide-post", url_name="hide-post")
    # def hide_post(self, request, pk):
    #     try:
    #         p = Post.objects.get(pk=pk)
    #         p.active = False
    #         p.save()
    #     except Post.DoesNotExist:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     return Response(status=status.HTTP_200_OK, data=PostSerializer(p, context={'request': request}).data)

    @action(methods=['post'], detail=True, url_path="tags")
    def add_tags(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get("tags")
            if tags is not None:
                for tag in tags:
                    t, _ = Tag.objects.get_or_create(name=tag)
                    post.tags.add(t)

                post.save()
                return Response(self.serializer_class(post).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True, url_path="like")
    def take_action(self, request, pk):
        try:
            action_type = int(request.data['type'])
        except Union[IndexError, ValueError]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            action = ActionPost.objects.create(type=action_type, user=request.user, post=self.get_object())

            return Response(ActionPostSerializer(action).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path="postview")
    def inc_view(self, request, pk):
        v, created = PostView.objects.get_or_create(post=self.get_object())
        v.views = F('views') + 1
        v.save()

        v.refresh_from_db()

        return Response(PostViewSerializer(v).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path="add_comment")
    def add_comment(self, request, pk):
        content = request.data.get('content')

        if content:
            comment = CommentPost.objects.create(content=content, post=self.get_object(), user=request.user)

            return Response(CommentPostSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


class TourViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    serializer_class = TourSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        tour = Tour.objects.filter(active = True)

        q = self.request.query_params.get('q')
        if q is not None:
            tour = tour.filter(name__icontains=q)

        return tour

    @action(methods=['post'], detail=True, url_path="rate")
    def rate(self, request, pk):
        try:
            rating = int(request.data['rating'])
        except Union[IndexError, ValueError]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            r = Rating.objects.create(rate=rating, tour=self.get_object(), user=request.user)

            return Response(RatingSerializer(r).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='add_comment')
    def add_comment(self, request, pk):
        content = request.data.get('content')

        if content:
            comment = CommentTour.objects.create(content=content, user=request.user, tour=self.get_object())

            return Response(CommentTourSerializer(comment).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class CommentPostViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = CommentPost.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentPostSerializer

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentTourViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = CommentTour.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentTourSerializer

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

# def index(request):
#     return render(request, template_name='index.html', context={
#         'name':'Cao Ngoc Cuong'
#     })

# def welcome(request, name):
#     return HttpResponse("hello" + str(name))
#
# def welcome2(request, year):
#     return HttpResponse("Regex test" + year)
#
#
# class TestView(View):
#     def get(self, request):
#         return HttpResponse("Hello this is my testing.")
#
#     def post(self, request):
#         pass