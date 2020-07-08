from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from authentication.models import UserProfile
from levels.filters import ClassFilter
from levels.forms import CreateClassForm
from levels.models import Class_uni
from students.models import Student


# Create your views here.

@login_required(login_url='teachers:login')
def levels_get(request):
    if request.user.is_staff:
        classes = Class_uni.objects.all()

        my_filter = ClassFilter(request.GET, queryset=classes)
        classes = my_filter.qs

        context = {
            "classes": classes
        }
        return render(request, '../templates/levels_grid_all.html', context)
    else:
        user_profile = UserProfile.objects.get(user_id=request.user.id)
        classe = user_profile.classes.all()

        my_filter = ClassFilter(request.GET, queryset=classe)
        classe = my_filter.qs

        context = {
            "classes": classe
        }
        return render(request, '../templates/levels_grid.html', context)


def levels_get_all(request):
    classes = Class_uni.objects.all()

    my_filter = ClassFilter(request.GET, queryset=classes)
    classes = my_filter.qs

    context = {
        "classes": classes
    }

    return render(request, '../templates/levels_grid_all.html', context)


def level_add(request):
    form = CreateClassForm()
    classe = Class_uni()

    if request.method == 'POST':
        form = CreateClassForm(request.POST, request.FILES, instance=classe)
        if form.is_valid():
            form.save()
            return redirect(reverse('levels:level-list-all'))
    else:
        form = CreateClassForm()

    context = {
        'form': form
    }

    return render(request, '../templates/level_add.html', context)


def level_details(request, class_id):
    classe = Class_uni.objects.get(id=class_id)
    students = Student.objects.filter(class_id=class_id)
    courses = classe.course.all()

    course_id = 0
    context = {
        'class': classe,
        'courses': courses,
        'students': students,
        'courseid': course_id
    }

    return render(request, '../templates/level_details.html', context)


def level_update(request, class_id):
    classe = Class_uni.objects.get(id=class_id)
    form = CreateClassForm(request.POST, request.FILES, instance=classe)

    if request.method == 'POST':
        form = CreateClassForm(request.POST, request.FILES, instance=classe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student successfully updated')
            return redirect(reverse('students:student-add'))
    else:
        form = CreateClassForm()

    context = {
        'classe': classe,
        'form': form
    }

    return render(request, '../templates/level_add.html', context)


def level_delete(request, class_id):
    classe = Class_uni.objects.get(id=class_id)
    classe.delete()
    messages.success(request, 'Classe successfully deleted')

    return redirect(reverse('levels:level-list-all'))
