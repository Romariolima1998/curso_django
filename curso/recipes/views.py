import os

from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404
from django.db.models import Q

from recipes.models import Recipe
from utils.pagination import make_pagination

# Create your views here.
PER_PAGES = int(os.environ.get('PER_PAGES', 6))


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    context = {'recipes': page_obj, 'pagination_range': pagination_range}

    return render(request, 'recipes/pages/home.html', context=context)


def recipe(request, id):
    content = get_object_or_404(Recipe, id=id, is_published=True)

    context = {
        'recipe': content,
        'is_detail_page': True,
        'title': f'{content.title} |'
        }
    return render(request, 'recipes/pages/recipe.html', context=context)


def category(request, id):
    # recipes = Recipe.objects.filter(category__id=id, is_published=True)
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=id,
        is_published=True
        ).order_by('-id'))
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    context = {
        'recipes': page_obj,
        'title': f'{recipes[0].category.name} - category |',
        'pagination_range': pagination_range
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
    
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGES)

    return render(request, 'recipes/pages/search.html', {
        'page_title': f'search for "{search_term}" |',
        'recipes': page_obj,
        'search_term': search_term,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}'
    })
