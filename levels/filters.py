import django_filters
from .models import *


class ClassFilter(django_filters.FilterSet):

    class Meta:
        model = Class_uni
        fields = '__all__'
