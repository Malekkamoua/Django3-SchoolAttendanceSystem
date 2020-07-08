from django.db import models
from courses.models import Course


# Create your models here.
class Class_uni(models.Model):
    name = models.CharField(max_length=120)  # max_length = required

    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.name
