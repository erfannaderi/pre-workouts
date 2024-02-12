from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from secureapp.forms import CreateUser


# Create your views here.
def home(request):
    return render(request, 'index.html')


def register(request):
    form = CreateUser
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')

    context = {'form': form}

    return render(request, 'register.html', context)


@login_required(login_url='two_factor:login')
def dashboard(request):
    return render(request, 'dashboard.html')


def logout(request):
    auth.logout(request)
    return redirect('')


def account_locked(request):

    return render(request, 'account-locked.html')
