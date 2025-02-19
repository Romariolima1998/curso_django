from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse

from utils.recipes.factory import make_recipe 
from recipes.models import Recipe

# Create your views here.

def home(request):
    # recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    recipes = get_list_or_404(Recipe.objects.filter(is_published=True).order_by('-id'))
    context= {'recipes': recipes}
    return render(request, 'recipes/pages/home.html', context=context)


def recipe(request, id):
    content = get_object_or_404(Recipe, id=id)

    context= {'recipe': content,
              'is_detail_page': True}
    return render(request, 'recipes/pages/recipe.html', context=context)


def category(request, id):
# recipes = Recipe.objects.filter(category__id=id, is_published=True)
    recipes = get_list_or_404(Recipe.objects.filter(category__id=id, is_published=True).order_by('-id'))
    context= {
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - category |'
        }
    return render(request, 'recipes/pages/category.html', context=context)
