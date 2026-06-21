from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from .forms import CustomUserForm 

def register_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True          
            user.save()                    
            return redirect('/')
    else:
        form = CustomUserForm()

    return render(request, 'authentication/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'authentication/login.html', {'error': 'Неправильний email або пароль!'})

    return render(request, 'authentication/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def user_list_view(request):
    if request.user.role != 1: return redirect('/')
    users = CustomUser.objects.all()
    return render(request, 'authentication/user_list.html', {'users': users})

def user_detail_view(request, user_id):
    if request.user.role != 1: return redirect('/')
    user = CustomUser.get_by_id(user_id)
    orders = user.orders.filter(end_at__isnull=True)
    return render(request, 'authentication/user_detail.html', {'user_obj': user, 'orders': orders})