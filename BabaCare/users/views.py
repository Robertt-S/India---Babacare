from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

# Create your views here.
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration sucessful"))
            return redirect('home')
            
    else:
        form = RegisterUserForm()
        
    return render(request,'users/register.html', {'form':form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("Houve um erro ao logar!"))
            return redirect('users:login')
    else:
        return render(request, 'users/login.html')
    

def logout_view(request):
    logout(request)
    messages.success(request, ("You're logged out!"))
    return redirect('home')