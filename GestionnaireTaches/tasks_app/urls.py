from . import views
from django.urls import path
from .views import TaskListView, TaskCreateView, signup_view,TaskUpdateView, TaskDeleteView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', TaskListView.as_view(), name='default'),  
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', TaskCreateView.as_view(), name='task_create'),
    path('create_category/', views.create_category, name='create_category'),
    # path('create_tag/', views.create_tag, name='create_tag'),
    path('signup/', signup_view, name='signup'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('category/update/<int:pk>/', views.update_category, name='update_category'),
    # path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),

    path('logout/', LogoutView.as_view(next_page='task_list'), name='logout'),  
    path('export-tasks/', views.export_tasks, name='export_tasks'),

]

  
