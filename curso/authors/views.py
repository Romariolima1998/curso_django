from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from authors.forms import RegisterForm, LoginForm

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
        else:
            messages.error(request, 'Invalid credentials')

    else:
        messages.error(request, 'Invalid username or password')

    return redirect('authors:login')

@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):

    logout(request)
    messages.success(request, 'Logout successfully')
 
    return redirect('authors:login')