from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def login_page(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user=user)
            return redirect('/home/')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request,'account/login.html')

def registration_page(request):
    form = RegistrationForm()
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            username = request.POST.get('username')
            password = request.POST.get('password1')
            user = authenticate(request, username=username,password=password)
            login(request, user=user)
            return redirect('/home/')
        
            
    context = {
        'form' : form,
    }
    return render(request,'account/registration.html', context)

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('/login/')