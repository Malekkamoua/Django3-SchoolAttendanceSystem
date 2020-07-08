from django.forms import ModelForm
from students.models import Student
from students.models import Attendance_detail
from levels.models import Class_uni
from django import forms


class StudentForm(ModelForm):
    first_name = forms.CharField(label='First name',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last name',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    cin = forms.IntegerField(label='CIN',
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(label='Date of birth',
                                    widget=forms.SelectDateWidget(
                                        attrs={'class': 'form-control date'}))
    email = forms.CharField(label='Email',
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.IntegerField(label='Phone',
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(label='Profile picture',
                                   widget=forms.FileInput(attrs={'class': 'form-control'}))

    class_id = forms.ModelChoiceField(queryset=Class_uni.objects.filter(), required=True,
                                      widget=forms.Select(attrs={'class': 'form-control c'}))

    class Meta:
        model = Student
        exclude = ()
