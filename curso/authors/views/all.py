from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseNotAllowed
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify


from authors.forms import RegisterForm, LoginForm, AuthorRecipeForm
from recipes.models import Recipe

# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data')

    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register.html', {
        'form': form,
        'form_action': reverse('authors:register_create')
        })


def register_create(request):
    if request.method != 'POST':
        raise Http404()
    FORM = request.POST
    request.session['register_form_data'] = FORM
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        del (request.session['register_form_data'])
        messages.success(request, 'User created successfully')
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request):
    login_form = LoginForm()
    return render(request, 'authors/pages/login.html', {
        'form': login_form,
        'form_action': reverse('authors:login_create')
    })


def login_create(request):
    if request.method != 'POST':
        raise Http404()

    form = LoginForm(request.POST)
    if form.is_valid():
        user_authenticated = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user_authenticated:
            login(request, user_authenticated)
            messages.success(request, 'Login successfully')
            return redirect(request.GET.get('next', 'authors:dashboard'))
        else:
            messages.error(request, 'Invalid credentials')

    else:
        messages.error(request, 'Invalid username or password')

    return redirect('authors:login')

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if request.method != 'POST':
        raise Http404()

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid credentials')
        return redirect('authors:login')

    logout(request)
    messages.success(request, 'Logout successfully')

    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
        )
    return render(request, 'authors/pages/dashboard.html', {
        'recipes': recipes,
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe(request, recipe_id):

    recipe = Recipe.objects.filter(
        is_published=False,
        id=recipe_id,
        author=request.user
    ).first()

    if not recipe:
        raise Http404()

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

        return redirect('authors:dashboard_recipe_edit', recipe_id=recipe_id)

    return render(request, 'authors/pages/dashboard_recipe.html', {
        'recipe': recipe,
        'form': form,
        # 'form_action': reverse('authors:dashboard_recipe', args=(recipe_id,))
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create(request):

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        )

    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.slug = slugify(recipe.title)
        recipe.save()

        messages.success(request, 'Recipe created successfully')
        return redirect('authors:dashboard_recipe_edit', recipe_id=recipe.id)

    return render(request, 'authors/pages/dashboard_recipe.html', {
        'form': form,
        # 'form_action': reverse('authors:dashboard_recipe', args=(recipe_id,))
    })

@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete(request, recipe_id):
    recipe = Recipe.objects.filter(
        is_published=False,
        id=recipe_id,
        author=request.user
    ).first()

    if not recipe:
        raise Http404()

    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe deleted successfully')
    else:
        return HttpResponseNotAllowed(['POST'])

    return redirect('authors:dashboard')
