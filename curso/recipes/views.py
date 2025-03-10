from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponse, Http404
from django.db.models import Q

from recipes.models import Recipe

# Create your views here.


def home(request):
    # recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {'recipes': recipes}
    return render(request, 'recipes/pages/home.html', context=context)


def recipe(request, id):
    content = get_object_or_404(Recipe, id=id, is_published=True)

    context = {'recipe': content,
              'is_detail_page': True}
    return render(request, 'recipes/pages/recipe.html', context=context)


def category(request, id):
    # recipes = Recipe.objects.filter(category__id=id, is_published=True)
    recipes = get_list_or_404(Recipe.objects.filter(category__id=id, is_published=True).order_by('-id'))
    context = {
        'recipes': recipes,
        'title': f'{recipes[0].category.name} - category |'
        }
    return render(request, 'recipes/pages/category.html', context=context)


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True
        ).order_by('-id')

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'search for "{search_term}" |',
        'recipes': recipes,
        'search_term': search_term
    })
