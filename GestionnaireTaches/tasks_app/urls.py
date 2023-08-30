from django.urls import path
from .views import TaskListView, TaskCreateView, signup_view,TaskUpdateView, TaskDeleteView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', TaskListView.as_view(), name='default'),  # URL par défaut vers la liste des tâches
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('signup/', signup_view, name='signup'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('logout/', LogoutView.as_view(next_page='task_list'), name='logout'),  # Redirige vers votre page de connexion

]

  
