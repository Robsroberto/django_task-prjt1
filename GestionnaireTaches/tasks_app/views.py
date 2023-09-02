from datetime import datetime
from .models import Task
from django.shortcuts import render, redirect
from django.urls import reverse,reverse_lazy

from django.views.generic import UpdateView, DeleteView
from django.views import View
from django.views.generic import ListView, CreateView

from .forms import TaskForm,CustomAuthenticationForm
from .forms import CustomUserCreationForm 

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth.models import User


# from django.contrib.auth.decorators import login_required

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

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user  # Associez la tâche à l'utilisateur actuel
    #     return super().form_valid(form)

    def form_valid(self, form):
        # Définir automatiquement created_by comme l'utilisateur connecté
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm  # Utilisez votre propre formulaire
    template_name = 'tasks_app/task_update.html'  # Créez ce template

    def get_success_url(self):
        return reverse('task_list')  # Rediriger après la modification vers la liste des tâches
    def form_valid(self, form):
        task = form.save(commit=False)

        # Vérifiez si la case à cocher "completed" a été cochée
        if task.completed:
            # Si elle a été cochée, mettez à jour la date de complétion
            task.completed_date = datetime.now() # Utilisez la date et l'heure actuelles
        else:
            # Si elle n'a pas été cochée, définissez la date de complétion sur None
            task.completed_date = None

        task.save()
        form.instance.created_by = self.request.user

        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
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
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('../login/')  # Rediriger vers la page des tâches après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'tasks_app/signup.html', {'form': form})


class CustomLogoutView(LogoutView):
    # next_page = reverse_lazy('tasks_app/task_list.html')  # Remplacez 'your_login_page' par le nom de votre page de connexion
    next_page = '/tasks/'  # Remplacez par l'URL vers laquelle vous souhaitez rediriger après la déconnexion




class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

