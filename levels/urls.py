from django.urls import path
from . import views

app_name = 'levels'

urlpatterns = [
    path('get/', views.levels_get, name='level-list'),
    path('get/all/', views.levels_get, name='level-list-all'),
    path('get/<int:class_id>', views.level_details, name='level-details'),
    path('add/', views.level_add, name='level-add'),
    path('update/<int:class_id>', views.level_update, name='level-update'),
    path('delete/<int:class_id>', views.level_delete, name='level-delete')
]