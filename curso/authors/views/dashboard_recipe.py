from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

from recipes.models import Recipe
from authors.forms import AuthorRecipeForm, RegisterForm

@method_decorator(login_required(
    login_url='authors:login',
    redirect_field_name='next'
), name='dispatch')
class DashboardRecipeList(ListView):
    model = Recipe
    template_name = 'authors/pages/dashboard.html'
    context_object_name = 'recipes'
    paginate_by = None
    ordering = '-id'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            author=self.request.user,
            is_published=False
        )
        return queryset

    
@method_decorator(login_required(
    login_url='authors:login',
    redirect_field_name='next'
), name='dispatch')
class DashboardRecipe(View):
    def get_recipe(self, recipe_id):
        recipe = None

        if recipe_id:
            recipe = Recipe.objects.filter(
                is_published=False,
                id=recipe_id,
                author=self.request.user
            ).first()

            if not recipe:
                raise Http404()

        return recipe

    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html', {
            'form': form,
        })

    def get(self, request, recipe_id=None):
        recipe = self.get_recipe(recipe_id)

        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form)

    def post(self, request, recipe_id=None):
        recipe = self.get_recipe(recipe_id)

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()

            messages.success(request, 'Recipe updated successfully')

            return redirect(
                'authors:dashboard_recipe_edit',
                recipe_id=recipe.id
                )

        return self.render_recipe(form)


@method_decorator(login_required(
    login_url='authors:login',
    redirect_field_name='next'
), name='dispatch')
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, request, recipe_id=None):
        recipe = self.get_recipe(recipe_id)

        recipe.delete()
        messages.success(request, 'Recipe deleted successfully')

        return redirect(reverse('authors:dashboard'))
