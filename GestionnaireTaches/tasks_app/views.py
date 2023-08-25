from django.shortcuts import render, redirect
from .models import Task
from django.views import View
from .forms import TaskForm
# Create your views here.

class TaskListView(View):
    def get(self, request):
        tasks = Task.objects.all()
        return render(request, 'tasks_app/task_list.html', {'tasks': tasks})

class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'tasks_app/task_form.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
        return render(request, 'tasks_app/task_form.html', {'form': form})
