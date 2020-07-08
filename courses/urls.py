from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('get/', views.course_get_all_teacher, name='course-get'),
    path('get/all', views.course_get_all, name='course-get-all'),
    path('get/<int:class_id>', views.course_get, name='course-list'),
    path('add/', views.course_add, name='course-add'),
    path('update/<int:course_id>', views.course_update, name='course-update'),
    path('delete/<int:course_id>', views.course_delete, name='course-delete')
]
