from django.urls import path
from .views import TaskListView, TaskCreateView, signup_view

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('signup/', signup_view, name='signup'),
]