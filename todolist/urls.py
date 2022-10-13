from django.urls import path
from todolist.views import *

app_name = 'todolist'

urlpatterns = [
    path('', show_todolist, name='show_todolist'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('create-task/', create_task, name='create_task'),
    path('change-task/<int:task_id>', change_task, name='change_task'),
    path('delete-task/<int:task_id>', delete_task, name='delete_task'),
    path('json/' , show_task_json, name='json'),
    path('add/', add_task_ajax, name='add'),
    path('delete/<int:task_id>', delete_task_ajax, name='delete'),
]
