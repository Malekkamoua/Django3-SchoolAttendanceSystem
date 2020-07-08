from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from courses.filters import CourseFilter
from courses.forms import CreateCourseForm
from authentication.models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
from courses.models import Course
from levels.models import Class_uni


@login_required(login_url='login')
def course_get_all_teacher(request):
    user_profile = UserProfile.objects.get(user_id=request.user.id)
    courses = user_profile.courses.all()

    my_filter = CourseFilter(request.GET, queryset=courses)
    courses = my_filter.qs

    context = {
        "courses": courses
    }
    return render(request, '../templates/course_grid.html', context)


@login_required(login_url='login')
def course_get_all(request):
    courses = Course.objects.all()

    my_filter = CourseFilter(request.GET, queryset=courses)
    courses = my_filter.qs

    context = {
        "courses": courses
    }
    return render(request, '../templates/course_grid_all.html', context)


def course_add(request):
    form = CreateCourseForm()
    course = Course()
    if request.method == 'POST':
        form = CreateCourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect(reverse('courses:course-get-all'))
    else:
        form = CreateCourseForm()

    context = {
        'form': form
    }
    return render(request, '../templates/course_add.html', context)


def course_update(request, course_id):
    course = Course.objects.get(id=course_id)
    form = CreateCourseForm(request.POST, request.FILES, instance=course)

    if request.method == 'POST':
        form = CreateCourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course successfully updated')
            return redirect(reverse('courses:course-get-all'))

    is_update = True

    context = {
        'course': course,
        'form': form,
        'is_update': is_update
    }

    return render(request, '../templates/course_add.html', context)


def course_get(request, class_id):
    classe = Class_uni.objects.get(id=class_id)
    courses = classe.course.all()

    context = {
        "courses": courses,
        "classid": class_id
    }
    return render(request, '../templates/course_grid.html', context)


def course_delete(request, course_id):

    course = Course.objects.get(id=course_id)
    course.delete()
    messages.success(request, 'Course successfully deleted')

    return redirect(reverse('courses:course-get-all'))
