from django.db import models
from authentication.models import UserProfile
from levels.models import Class_uni
from courses.models import Course


# Create your models here.
class Student(models.Model):
    cin = models.IntegerField()
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone = models.IntegerField(null=False, default="711111111")
    email = models.CharField(max_length=255, default="student@mail.com")
    profile_pic = models.ImageField(default="no_image.png", null=False, blank=False)

    class_id = models.ForeignKey(Class_uni, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.first_name


class Attendance_image(models.Model):
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classe = models.ForeignKey(Class_uni, on_delete=models.CASCADE)
    nb_p = models.IntegerField(null=False)

    attendance_pic = models.ImageField(default="no_image.png", null=False, blank=False, upload_to='attendance')

    date = models.DateTimeField(auto_now_add=True, blank=True)


class Attendance_detail(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    classe = models.ForeignKey(Class_uni, on_delete=models.CASCADE)

    present = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True, blank=True)


class Elimination(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    nb_absences = models.IntegerField()
    eliminated = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)
