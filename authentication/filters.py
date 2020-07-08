import django_filters
from .models import *


class TeacherFilter(django_filters.FilterSet):

    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['profile_pic']

