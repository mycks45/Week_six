from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.sessions.models import Session
from django.views.decorators.cache import cache_control
# from .models import Users

from django.contrib import messages

from .forms import CreateUserForm
from  .decorators import unauthenticated_user, allowed_user
from .filters import Userfilter
# Create your views here.


# This function render home page
@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'customer'])
def home(request):
    return render(request, 'home.html')


# This function handle main login
@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "incorrect username or password")
            
    context = {}
    return render(request, 'login.html', context)


# This fuunction handle Logout
def logoutUser(request):
    logout(request)
    return redirect('login')


# This function add new user and group it as customer
@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Created user '+ username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'register.html', context)


# This function show admin panel with user 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_panel(request):
    if request.session.has_key('is_logged'):
        customers = User.objects.all().order_by('id')
        myFilter = Userfilter(request.GET, queryset=customers)
        customers = myFilter.qs
        context = {'customers':customers, 'myFilter':myFilter}
        return render(request, 'adminPanel.html', context)
    
    if request.method== 'POST':
        admin = 'anfus'
        pwd = 'qazxcvbnm,'
        if admin == request.POST['admin'] and pwd == request.POST['pwd']:
            request.session['is_logged'] = True
            customers = User.objects.all()
            myFilter = Userfilter(request.GET, queryset=customers)
            customers = myFilter.qs
            context = {'customers':customers, 'myFilter':myFilter}
            return render(request, 'adminPanel.html', context)
        else:
            messages.info(request, "incorrect username or password")
    else:       
        return render(request, 'adminPanelForm.html')


# This fuunction handle Logout admin in admin panel
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logoutadmin(request):
    del request.session['is_logged']
    return redirect('admin_panel')


# This function add new user from admin panel
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminPanelUser(request):
    if request.session.has_key('is_logged'):
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)

            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name='customer')
                user.groups.add(group)

                messages.success(request, 'Created user '+ username)
                return redirect('admin_panel')
            else:
                messages.info(request, "password didn't match")
        context = {'form':form}   
        return render(request, 'adminPanelUser.html', context)
    else:
        return redirect('admin_panel')

# This function update user information in admin panel 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updateUser(request, pk):
    if request.session.has_key('is_logged'):
        user = User.objects.get(id=pk)
        form = CreateUserForm(instance=user)
        if request.method == 'POST':
            form = CreateUserForm(request.POST, instance=user)

            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name='customer')
                user.groups.add(group)

                messages.success(request, 'Created user '+ username)
                return redirect('admin_panel')

        context = {'form':form}
        return render(request, 'adminPanelUser.html', context)
    else:
        return redirect('admin_panel')

# This function delete user in admin Panel 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def deleteUser(request, pk):
    if request.session.has_key('is_logged'):
        user = User.objects.get(id=pk)
        if request.method == 'POST':
            user.delete()
            return redirect('admin_panel')
        context = {'item':user}
        return render(request, 'delete.html', context)
    else:
        return redirect('admin_panel')


