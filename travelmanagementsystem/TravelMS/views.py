from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from django.views import View
from rest_framework import viewsets, permissions
from .serializers import PostSerializer



class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated()]

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