from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    context= {'ola': 'mundo'}
    return render(request, 'recipes/pages/home.html', context=context)

