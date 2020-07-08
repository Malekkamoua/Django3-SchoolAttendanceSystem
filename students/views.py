from datetime import datetime
from random import randint

from django.shortcuts import render, redirect
from django.urls import reverse

from authentication.models import UserProfile
from courses.models import Course
from students.forms import StudentForm
from students.models import Student, Attendance_detail, Elimination, Attendance_image
from django.contrib import messages

from levels.models import Class_uni
from django.utils import timezone
from students.filters import StudentFilter

from django.core.mail import send_mail
from django.conf import settings

import face_recognition
from PIL import Image, ImageDraw
from django.utils.crypto import get_random_string


# Create your views here.

def email_warning(request, email, course_id):
    course = Course.objects.get(id=course_id)
    course_name = course.name

    subject = 'Elimination warning !'
    message = 'Dear student, please beware because you are running out of permitted absences number for ' + course_name
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [
        email,
    ]
    send_mail(subject, message, email_from, recipient_list)
    return render(request, '../templates/student_add.html')


def student_add(request):
    student = Student()
    form = StudentForm()

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student successfully added')
            return redirect(reverse('students:student-add'))

    context = {
        'form': form
    }
    return render(request, '../templates/student_add.html', context)


def students_get(request, class_id, course_id):
    students = Student.objects.filter(class_id=class_id)
    classe = Class_uni.objects.get(id=class_id)

    my_filter = StudentFilter(request.GET, queryset=students)
    students = my_filter.qs

    test = False

    today = timezone.datetime.today()
    attendance_today = Attendance_detail.objects.filter(date=today, course_id=course_id, classe_id=class_id)

    nb = attendance_today.count()

    if nb is not 0:
        test = True
        presents = 0

        for p in attendance_today:
            if p.present is True:
                presents = presents + 1

        pourcentage = round((presents / nb) * 100, 2)

        context = {
            "filter": my_filter,
            "students": students,
            "classe": classe,
            "classid": class_id,
            "courseid": course_id,
            "presents": presents,
            "pourcentage": pourcentage,
            'test': test
        }
        return render(request, '../templates/students_list.html', context)

    context = {
        "filter": my_filter,
        "students": students,
        "classe": classe,
        "classid": class_id,
        "courseid": course_id,
        'test': test
    }

    return render(request, '../templates/students_list.html', context)


def profile(request, student_id):
    queryset = Student.objects.get(id=student_id)
    context = {
        "student": queryset
    }
    return render(request, '../templates/student_profile.html', context)


def student_delete(request, student_id, class_id):
    student = Student.objects.get(id=student_id)
    student.delete()
    messages.success(request, 'Student successfully deleted')

    return redirect(reverse('levelss:level-details', kwargs={'class_id': class_id}))


def student_update(request, student_id):
    student = Student.objects.get(id=student_id)
    class_id = student.class_id

    form = StudentForm(request.POST or None, request.FILES, instance=student)

    if request.method == 'POST':
        form = StudentForm(request.POST or None, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student successfully updated')
            return redirect(reverse('students:student-add'))
    else:
        form = StudentForm()

    is_update = True

    context = {
        'student': student,
        'class': class_id,
        'form': form,
        'is_update': is_update
    }

    return render(request, '../templates/student_update.html', context)


def mark_attendance_manually(request):

    if request.method == 'POST':
        present_students_ids = request.POST.getlist('p')

        course_id = request.POST.get('course_id')
        course = Course.objects.get(id=course_id)

        course_nb_absences = course.absences_number

        class_id = request.POST.get('class_id')
        classe = Class_uni.objects.get(id=class_id)
        all_students = Student.objects.filter(class_id=class_id)

        all_students_ids = []

        for s in all_students:
            all_students_ids.append(s.id)

        absent_students_ids = list(set(all_students_ids) - set(map(int, present_students_ids)))

        for student_id in present_students_ids:

            student = Student.objects.get(id=student_id)
            attendance_sheet = Attendance_detail(student=student, course=course, present=True, date=datetime.now,
                                                 classe=classe)
            attendance_sheet.save()

            elimination_sheet = Elimination.objects.filter(student_id=student.id).last()

            if elimination_sheet:
                nb_absences = elimination_sheet.nb_absences

                if course_nb_absences - elimination_sheet.nb_absences <= 0:
                    is_eliminated = True

                    elimination_sheet.student = student
                    elimination_sheet.course = course
                    elimination_sheet.eliminated = is_eliminated
                    elimination_sheet.nb_absences = nb_absences
                    elimination_sheet.date = timezone.now()

                    elimination_sheet.save()

            elif elimination_sheet is None:
                elimination_sheet = Elimination(student=student, course=course, eliminated=False,
                                                nb_absences=0)
                elimination_sheet.save()

        for student_id in absent_students_ids:
            student = Student.objects.get(id=student_id)

            attendance_sheet = Attendance_detail(student=student, course=course, present=False, date=datetime.now,
                                                 classe=classe)
            attendance_sheet.save()

            elimination_sheet = Elimination.objects.filter(student_id=student.id).last()

            if elimination_sheet:
                nb_absences = elimination_sheet.nb_absences + 1

                if course_nb_absences - elimination_sheet.nb_absences <= 0:
                    is_eliminated = True

                    elimination_sheet.student = student
                    elimination_sheet.course = course
                    elimination_sheet.eliminated = is_eliminated
                    elimination_sheet.nb_absences = nb_absences
                    elimination_sheet.date = timezone.now()

                    elimination_sheet.save()
                else:
                    elimination_sheet.student = student
                    elimination_sheet.course = course
                    elimination_sheet.nb_absences = nb_absences
                    elimination_sheet.date = timezone.now()

                    elimination_sheet.save()

                    if course_nb_absences - nb_absences == 1:
                        email_warning(request, student.email, course_id)

            elif elimination_sheet is None:
                elimination_sheet = Elimination(student=student, course=course, eliminated=False,
                                                nb_absences=1, date=timezone.now())
                elimination_sheet.save()

    messages.success(request, 'Student successfully marked')
    return redirect(reverse('students:students-list', kwargs={'class_id': class_id, 'course_id': course_id}), )


def mark_attendance_automatically(request):
    if request.method == 'POST':

        course_id = request.POST.get('course_id')
        class_id = request.POST.get('class_id')
        teacher_id = request.POST.get('teacher_id')
        attendance_pic = request.FILES.get('pic')

        course = Course.objects.get(id=course_id)
        classe = Class_uni.objects.get(id=class_id)
        teacher = UserProfile.objects.get(user_id=teacher_id)

        course_nb_absences = course.absences_number

        all_students = Student.objects.filter(class_id=class_id)

        students_encodings = []
        students_names = []
        all_students_ids = []
        present_students_idss = []

        for s in all_students:
            pic = str(s.profile_pic)

            url = "static/images/uploads/" + pic

            image_of_student = face_recognition.load_image_file(url)
            student_face_encoding = face_recognition.face_encodings(image_of_student)[0]
            students_encodings.append(student_face_encoding)

            last_name = s.last_name
            first_name = s.first_name
            name = last_name + ' ' + first_name
            students_names.append(name)

            all_students_ids.append(s.id)

        # Load attendance image to find faces in
        attendance_image = face_recognition.load_image_file(attendance_pic)

        # Find faces in attendance image
        face_locations = face_recognition.face_locations(attendance_image)
        face_encodings = face_recognition.face_encodings(attendance_image, face_locations)

        # count faces
        nb_p = len(face_locations)

        # Convert to PIL format
        pil_image = Image.fromarray(attendance_image)

        # Create as ImageDraw instance
        draw = ImageDraw.Draw(pil_image)

        # Loop through faces in test image
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(students_encodings, face_encoding)

            name = "Unknown Person"

            # If match
            if True in matches:
                first_match_index = matches.index(True)
                name = students_names[first_match_index]
                student_id = all_students_ids[first_match_index]
                present_students_idss.append(student_id)

                student = Student.objects.get(id=student_id)
                attendance_sheet = Attendance_detail(student=student, course=course, present=True, date=datetime.now,
                                                     classe=classe)
                attendance_sheet.save()

                elimination_sheet = Elimination.objects.filter(student_id=student.id).last()

                if elimination_sheet:
                    nb_absences = elimination_sheet.nb_absences

                    if course_nb_absences - elimination_sheet.nb_absences <= 0:
                        is_eliminated = True

                        elimination_sheet.student = student
                        elimination_sheet.course = course
                        elimination_sheet.eliminated = is_eliminated
                        elimination_sheet.nb_absences = nb_absences
                        elimination_sheet.date = timezone.now()

                        elimination_sheet.save()

                elif elimination_sheet is None:
                    elimination_sheet = Elimination(student=student, course=course, eliminated=False,
                                                    nb_absences=0)
                    elimination_sheet.save()

            # Draw box
            draw.rectangle(((left, top), (right, bottom)), outline=(255, 255, 0))

            # Draw label
            text_width, text_height = draw.textsize(name)
            draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(255, 255, 0),
                           outline=(255, 255, 0))
            draw.text((left + 6, bottom - text_height - 5), name, fill=(0, 0, 0))

        del draw

        all_students_ids = []
        for s in all_students:
            all_students_ids.append(s.id)

        absent_students_ids = list(set(all_students_ids) - set(map(int, present_students_idss)))

        for student_id in absent_students_ids:
            student = Student.objects.get(id=student_id)

            attendance_sheet = Attendance_detail(student=student, course=course, present=False, date=datetime.now,
                                                 classe=classe)
            attendance_sheet.save()

            elimination_sheet = Elimination.objects.filter(student_id=student.id).last()

            if elimination_sheet:
                nb_absences = elimination_sheet.nb_absences + 1

                if course_nb_absences - elimination_sheet.nb_absences <= 0:
                    is_eliminated = True

                    elimination_sheet.student = student
                    elimination_sheet.course = course
                    elimination_sheet.eliminated = is_eliminated
                    elimination_sheet.nb_absences = nb_absences
                    elimination_sheet.date = timezone.now()

                    elimination_sheet.save()
                else:
                    elimination_sheet.student = student
                    elimination_sheet.course = course
                    elimination_sheet.nb_absences = nb_absences
                    elimination_sheet.date = timezone.now()

                    elimination_sheet.save()

                    if course_nb_absences - nb_absences == 1:
                        email_warning(request, student.email, course_id)

            elif elimination_sheet is None:
                elimination_sheet = Elimination(student=student, course=course, eliminated=False,
                                                nb_absences=1, date=timezone.now())
                elimination_sheet.save()

        # Display image
        pil_image.show()

        # Save image
        n = get_random_string(length=7)
        image_name = classe.name + '_' + course.name + '_' + course.name + '_' + n + '.png'
        pil_image.save(image_name)

        attendance_image = Attendance_image(teacher=teacher, course=course, classe=classe, attendance_pic=image_name,
                                            nb_p=nb_p,
                                            date=timezone.now())
        attendance_image.save()

    messages.success(request, 'Student successfully marked')
    return redirect(reverse('students:students-list', kwargs={'class_id': class_id, 'course_id': course_id}), )


def stats(request, course_id, class_id, teacher_id):
    teacher = UserProfile.objects.get(user_id=teacher_id)

    attendance_details = Attendance_image.objects.filter(course_id=course_id, classe_id=class_id, teacher_id=teacher.id)
    context = {
        'details': attendance_details
    }

    return render(request, '../templates/students_stats.html', context)


def stats_details(request, detail_id):

    image = Attendance_image.objects.get(id=detail_id)
    detail_date = image.date
    fiche = Attendance_detail.objects.filter(date=detail_date)

    students_info = []
    etat_student = []

    for d in fiche:
        student = Student.objects.get(id=d.student_id)
        students_info.append(student)
        etat_student.append(d.present)

    classe = Class_uni.objects.get(id=image.classe_id)
    students = Student.objects.filter(class_id=classe.id)

    nb_students_total = len(students)

    pourcentage = round(image.nb_p / nb_students_total * 100, 2)
    rest = 100 - pourcentage

    context = {
        'detail': image,
        'studentss': students_info,
        'date': detail_date,
        'pourcentage': pourcentage,
        'rest': rest
    }

    return render(request, '../templates/students_stats_details.html', context)
