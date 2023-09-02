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
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth.models import User

from django.http import JsonResponse


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
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm 
    template_name = 'tasks_app/task_update.html'  
    def get_success_url(self):
        return reverse('task_list')  
    def form_valid(self, form):
        task = form.save(commit=False)

        if task.completed:
            task.completed_date = datetime.now() 
        else:
           
            task.completed_date = None

        task.save()
        form.instance.created_by = self.request.user

        return super().form_valid(form)
    
  

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})




def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('../logout/')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'tasks_app/signup.html', {'form': form})


class CustomLogoutView(LogoutView):
    # next_page = reverse_lazy('tasks_app/task_list.html')  
    next_page = '/tasks/'  



class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

