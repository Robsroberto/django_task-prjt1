from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Task
from django.views import View
from django.views.generic import ListView, CreateView
from .forms import TaskForm
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
# Create your views here.


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'tasks_app/task_list.html'
    context_object_name = 'tasks'

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks_app/task_form.html'
    success_url = '/tasks/'




class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm  # Utilisez votre propre formulaire
    template_name = 'tasks_app/task_update.html'  # Créez ce template

    def get_success_url(self):
        return reverse('task_list')  # Rediriger après la modification vers la liste des tâches

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks_app/task_confirm_delete.html'  # Créez ce template

    def get_success_url(self):
        return reverse('task_list')  # Rediriger après la suppression vers la liste des tâches

# class TaskListView(View):
#     def get(self, request):
#         tasks = Task.objects.all()
#         return render(request, 'tasks_app/task_list.html', {'tasks': tasks})


# class TaskCreateView(View):
#     def get(self, request):
#         form = TaskForm()
#         return render(request, 'tasks_app/task_form.html', {'form': form})

#     def post(self, request):
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('task_list')
#         return render(request, 'tasks_app/task_form.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks_list')  # Rediriger vers la page des tâches après l'inscription
    else:
        form = UserCreationForm()
    return render(request, 'tasks_app/signup.html', {'form': form})


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('tasks_app/task_list.html')  # Remplacez 'your_login_page' par le nom de votre page de connexion

# Utilisez CustomLogoutView dans urls.py comme indiqué ci-dessus
