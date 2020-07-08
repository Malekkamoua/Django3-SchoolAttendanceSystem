from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from authentication.filters import TeacherFilter
from authentication.models import UserProfile
from authentication.forms import SignUpForm, CreateTeacherForm


# Create your views here.

def registerPage(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES, )
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created for ' + user)
            return redirect(reverse('teachers:create-profile'))
    else:
        form = SignUpForm()

    context = {
        'form': form
    }
    return render(request, '../templates/register.html', context)


def createTeacherProfile(request):
    form = CreateTeacherForm()

    if request.method == 'POST':
        form = CreateTeacherForm(request.POST, request.FILES, )
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('first_name')
            messages.success(request, 'Teacher profile was successfully created for ' + user)
    else:
        form = CreateTeacherForm()

    context = {
        'form': form
    }
    return render(request, '../templates/create_teacher_profile.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('teachers:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(reverse('levels:level-list'))
        else:
            messages.warning(request, 'Username or password is incorrect')

    return render(request, '../templates/login.html')


def logoutUser(request):
    logout(request)
    return redirect('teachers:login')


@login_required(login_url='teachers:login')
def home(request):
    return render(request, '../templates/home.html')


@login_required(login_url='teachers:login')
def teachers_get(request):
    queryset = UserProfile.objects.all()

    my_filter = TeacherFilter(request.GET, queryset=queryset)
    queryset = my_filter.qs

    context = {
        "teachers": queryset
    }

    return render(request, '../templates/teachers_list.html', context)


@login_required(login_url='teachers:login')
def profile(request, teacher_id):
    queryset = UserProfile.objects.get(id=teacher_id)
    context = {
        "teacher": queryset
    }
    return render(request, '../templates/teacher_profile.html', context)


@login_required(login_url='teachers:login')
def profile_update(request, teacher_id):
    user = UserProfile.objects.get(id=teacher_id)

    form = CreateTeacherForm(request.POST, request.FILES, instance=user)

    if request.method == 'POST':
        form = CreateTeacherForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile successfully updated')
            return redirect(reverse('teachers:profile'))
    else:
        form = CreateTeacherForm()

    context = {
        'form': form,
        'teacher': user
    }

    return render(request, '../templates/teacher_profile.html', context)


@login_required(login_url='teachers:login')
def teacher_delete(request, teacher_id):
    teacher = UserProfile.objects.get(id=teacher_id)
    user = User.objects.get(id=teacher.user_id)
    teacher.delete()
    user.delete()

    messages.success(request, 'Teacher successfully deleted')

    return redirect(reverse('teachers:teachers-list'))
