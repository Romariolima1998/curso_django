from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth import authenticate, login, logout

from recipes.models import Recipe
from authors.forms import AuthorRecipeForm, RegisterForm, LoginForm


class LoginView(FormView):
    template_name = 'authors/pages/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('authors:dashboard')

    def form_valid(self, form):
        user_authenticated = authenticate(
            self.request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if user_authenticated:
            login(self.request, user_authenticated)
            messages.success(self.request, 'Login successfully')
            return super().form_valid(form)

        messages.error(self.request, 'Invalid credentials')
        return redirect('authors:login')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)


class LogoutView(View):
    @method_decorator(login_required(
        login_url='authors:login',
        redirect_field_name='next'
    ))
    def post(self, request, *args, **kwargs):
        if request.POST.get('username') != request.user.username:
            messages.error(request, 'Invalid credentials')
            return redirect('authors:login')

        logout(request)
        messages.success(request, 'Logout successfully')

        return redirect('authors:login')


class UserRegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'authors/pages/register.html'
    success_url = reverse_lazy('authors:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(self.request, 'User created successfully')
        return super().form_valid(form)
