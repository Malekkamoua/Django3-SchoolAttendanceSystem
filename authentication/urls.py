from django.urls import path

from .views import (home, registerPage, loginPage, logoutUser, profile, teachers_get,createTeacherProfile, profile_update, teacher_delete)

app_name = "teachers"

urlpatterns = [
    path('', home, name="home"),
    path('all/', teachers_get, name='teachers-list'),
    path('profile/<int:teacher_id>', profile, name='profile'),

    path('update/<int:teacher_id>/', profile_update, name='teacher-update'),
    path('del/<int:teacher_id>/', teacher_delete, name='teacher-delete'),

    path('register/', registerPage, name="register"),
    path('create/teacher/', createTeacherProfile, name="create-profile"),

    path('login/', loginPage, name="login"),
    path('logout/', logoutUser, name="logout")
]
