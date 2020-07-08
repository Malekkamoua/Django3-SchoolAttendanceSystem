from django.db import models


# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=120)  # max_length = required
    absences_number = models.IntegerField()

    def __str__(self):
        return self.name
