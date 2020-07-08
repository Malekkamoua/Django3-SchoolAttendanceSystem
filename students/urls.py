from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('add/', views.student_add, name='student-add'),
    path('update/<int:student_id>/', views.student_update, name='student-update'),
    path('del/<int:student_id>/<int:class_id>/', views.student_delete, name='student-delete'),
    path('profile/<int:student_id>', views.profile, name='student-profile'),
    path('all/<int:class_id>/<int:course_id>', views.students_get, name='students-list'),
    path('mark/', views.mark_attendance_manually, name="student-attendance-mark"),
    path('mark/auto/', views.mark_attendance_automatically, name="student-attendance-mark-automatically"),

    path('email/', views.email_warning, name="email-service"),
    path('stats/<int:course_id>/<int:class_id>/<int:teacher_id>', views.stats, name='students-stats'),
    path('stats/details/<int:detail_id>', views.stats_details, name="students-stats-details")
]
