from django.shortcuts import render, redirect
from django.http import Http404

from django.contrib import messages


from authors.forms import RegisterForm

# Create your views here.


def register_view(request):
    register_form_data = request.session.get('register_form_data')

    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register.html', {'form': form})


def register_create(request):
    if request.method != 'POST':
        raise Http404()
    FORM = request.POST
    request.session['register_form_data'] = FORM
    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
        del(request.session['register_form_data'])
        messages.success(request, 'User created successfully')

    return redirect('authors:register')
