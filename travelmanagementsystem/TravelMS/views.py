from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


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