from django.forms import ModelForm
from levels.models import Class_uni
from courses.models import Course
from django import forms


class CreateClassForm(ModelForm):

    name = forms.CharField(label='Name',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    course = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), required=True, widget=forms.SelectMultiple(attrs={'class': 'form-control c'}))

    class Meta:
        model = Class_uni
        fields = '__all__'
