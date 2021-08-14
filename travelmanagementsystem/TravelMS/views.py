from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, permissions, status, generics

from .models import Post, Tag, User
from .serializers import PostSerializer, TagSerializer, UserSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def get_permissions(self):
    #     if self.action == 'list':
    #         return [permissions.AllowAny()]
    #
    #     return [permissions.IsAuthenticated()]

    @action(methods=['post'], detail=True, url_path="hide-post", url_name="hide-post")
    def hide_post(self, request, pk):
        try:
            p = Post.objects.get(pk=pk)
            p.active = False
            p.save()
        except Post.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK, data=PostSerializer(p, context={'request': request}).data)



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]


def index(request):
    return render(request, template_name='index.html', context={
        'name':'Cao Ngoc Cuong'
    })

def welcome(request, name):
    return HttpResponse("hello" + str(name))

def welcome2(request, year):
    return HttpResponse("Regex test" + year)


class TestView(View):
    def get(self, request):
        return HttpResponse("Hello this is my testing.")

    def post(self, request):
        pass