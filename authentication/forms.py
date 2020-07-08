from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from authentication.models import UserProfile
from levels.models import Class_uni
from courses.models import Course


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class CreateTeacherForm(ModelForm):
    first_name = forms.CharField(label='First name',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Last name',
                                widget=forms.TextInput(attrs={"placeholder": "Last_name", 'class': 'form-control'}))
    cin = forms.IntegerField(label='CIN',
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))

    date_of_birth = forms.DateField(label='Date of birth',
                                    widget=forms.SelectDateWidget(
                                        attrs={'class': 'form-control date'}))

    phone = forms.IntegerField(label='Phone',
                               widget=forms.NumberInput(attrs={'class': 'form-control'}))
    profile_pic = forms.ImageField(label='Profile picture',
                                   widget=forms.FileInput(attrs={'class': 'form-control'}))

    courses = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), required=True,
                                             widget=forms.SelectMultiple(attrs={'class': 'form-control c'}))

    classes = forms.ModelMultipleChoiceField(queryset=Class_uni.objects.all(), required=True,
                                             widget=forms.SelectMultiple(attrs={'class': 'form-control c'}))

    class Meta:
        model = UserProfile
        fields = "__all__"
