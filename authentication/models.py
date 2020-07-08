from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from levels.models import Class_uni
from courses.models import Course


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+')
    username = None

    cin = models.IntegerField()
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    account_type = models.CharField(max_length=255, null=False , default="teacher")
    profile_pic = models.ImageField(default="no_image.png", null=False, blank=False)

    USERNAME_FIELD = 'first_name'
    REQUIRED_FIELDS = []

    classes = models.ManyToManyField(Class_uni)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.first_name
