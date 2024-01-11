from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserSignupForm, UserSigninForm, UserUpdateForm
from .models import User
from connections.models import UserCourse
from django.contrib import messages
from django.shortcuts import get_object_or_404


# user signup and save user to database
def user_signup(request):
    error = ''
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()

            if form is not None:
                print('user created successfully')
            else:
                print('user not created')

            return redirect('login')
        else:
            error = "Ma'lumotlar to'g'ri kiritilmagan"
    else:
        form = UserSignupForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'auth/register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserSigninForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            print(username, password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Username or password is incorrect')
                return redirect('login')
    else:
        form = UserSigninForm()
    context = {
        'form': form
    }
    return render(request, 'auth/login.html', context)


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('dashboard')


@login_required(login_url='login')
def profile_page(request):
    user_profile = User.objects.get(id=request.user.id)
    enrolled_courses = UserCourse.objects.filter(user=request.user.id)
    context = {
        'user_profile': user_profile,
        'enrolled_courses': enrolled_courses
    }
    return render(request, 'auth/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    user_profile = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            print('user updated successfully', form.cleaned_data)
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user_profile)
    context = {
        'form': form,
        'user_profile': user_profile
    }
    return render(request, 'auth/edit_profile.html', context)
