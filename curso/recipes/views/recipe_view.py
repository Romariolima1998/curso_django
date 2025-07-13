import os

from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404
from django.db.models import Q
# from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils import translation


from recipes.models import Recipe
from tag.models import Tag
from utils.pagination import make_pagination
from django.utils.translation import gettext as _

# Create your views here.
PER_PAGES = int(os.environ.get('PER_PAGES', 6))


def theory(request, *args, **kwargs):
    context = {}
    return render(request, 'recipes/pages/theory.html', context)


class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/pages/home.html'
    context_object_name = 'recipes'
    paginate_by = None

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        queryset = queryset.prefetch_related('tags', 'author__profile')
        return queryset
        # return Recipe.objects.filter(is_published=True).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, context.get('recipes'), PER_PAGES
            )

        html_language = translation.get_language()
        context['pagination_range'] = pagination_range
        context['recipes'] = page_obj
        context['html_language'] = html_language
        return context


class RecipeCategoryView(RecipeListView):
    template_name = 'recipes/pages/category.html'
    context_object_name = 'recipes'
    paginate_by = None
    ordering = '-id'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            category__id=self.kwargs.get('id'),
            is_published=True
            )

        if not queryset:
            raise Http404()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_translation = _('category')
        context['title'] = f'{context.get("recipes")[0].category.name} -' \
            f' {category_translation} |'
        return context


class SearchListView(RecipeListView):
    template_name = 'recipes/pages/search.html'
    context_object_name = 'recipes'
    paginate_by = None
    ordering = '-id'

    def get_queryset(self):
        search_term = self.request.GET.get('q', '').strip()
        if not search_term:
            raise Http404()

        queryset = super().get_queryset()
        queryset = queryset.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
            is_published=True 
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()

        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = f'Search for "{search_term}" |'
        context['search_term'] = search_term
        context['additional_url_query'] = f'&q={search_term}'
        return context


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'recipes/pages/recipe.html'
    context_object_name = 'recipe'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_title'] = f'{context.get("recipe").title} |'
        context['is_detail_page'] = True
        return context


class TagListView(RecipeListView):
    template_name = 'recipes/pages/tags.html'
    context_object_name = 'recipes'
    paginate_by = None
    ordering = '-id'

    def get_queryset(self, *args, **kwargs):

        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            tags__slug=self.kwargs.get('slug'),
            is_published=True
        )
        return queryset

    def get_context_data(self, *args, **kwargs):
        search_term = Tag.objects.filter(slug=self.kwargs.get('slug'))
        if not search_term:
            search_term = 'No recipes found'
        else:
            search_term = f'{search_term[0].name} - tag |'

        context = super().get_context_data(*args, **kwargs)

        context['page_title'] = f'"{search_term}" |'

        return context
