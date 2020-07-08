import django_filters
from django_filters import DateFilter, CharFilter

from .models import *


class StudentFilter(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['profile_pic', 'email', 'class_id', 'phone', 'date_of_birth','name']
