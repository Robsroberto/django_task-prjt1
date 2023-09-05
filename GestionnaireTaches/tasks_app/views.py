import json
import csv
from .forms import CategoryForm, TaskForm, CustomAuthenticationForm,CustomUserCreationForm 

from datetime import datetime

from .models import Task,Category


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse,reverse_lazy

from django.views.generic import UpdateView, DeleteView,ListView, CreateView
from django.views import View
from django.core.paginator import Paginator

# from django.core.paginator import EmptyPage, PageNotAnInteger

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView,LoginView
# from django.contrib.auth.models import User


from django.db.models import Q

from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect


# from django.contrib.auth.decorators import login_required

# Create your views here.


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'tasks_app/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10  

    def get_queryset(self):
        queryset = Task.objects.filter(created_by=self.request.user)

        # Filtrer par état (terminé ou non)
        status = self.request.GET.get('status')
        if status == 'completed':
            queryset = queryset.filter(completed=True)
        elif status == 'not_completed':
            queryset = queryset.filter(completed=False)

        # Filtrer par date
        due_date = self.request.GET.get('due_date')
        if due_date:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')  

            # Filtrer les tâches avec une date de création ou une date de fin correspondante
            queryset = queryset.filter(
                Q(created_at__date=due_date) | Q(completed_date__date=due_date)
            )

        # Trier par date de création par défaut
        sort_by = self.request.GET.get('sort_by', 'created_at')
        if sort_by == 'created_at':
            queryset = queryset.order_by('-created_at')  

      
        # paginator = Paginator(queryset, self.paginate_by)
        # page = self.request.GET.get('page')

        # tasks = paginator.get_page(page)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.object_list, self.paginate_by)
        
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)

        context['page'] = page
        return context

def create_category(request):
    categories = Category.objects.all() 

    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return redirect('/tasks/')  
    else:
        category_form = CategoryForm()

    return render(request, 'tasks_app/category_form.html', {'category_form': category_form, 'categories': categories})




# @csrf_protect
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks_app/task_form.html'
    success_url = '/tasks/'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.created_by = self.request.user

        task.save()

        tag_names = form.cleaned_data['tags']
        if tag_names:
            for tag_name in tag_names:
                task.tags.add(tag_name)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['due_date_field'] = self.form_class().fields['due_date']
        return context



# @csrf_protect
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

        existing_due_date = Task.objects.get(pk=task.pk).due_date
        if not task.due_date:
            task.due_date = existing_due_date
        task.save()
        form.instance.created_by = self.request.user

        return super().form_valid(form)
    
  

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})



# @csrf_protect

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


# @csrf_protect

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.user.is_authenticated:
            if not self.request.session.get('welcome_message_shown', False):
                messages.success(self.request, "Bienvenue, {} !".format(self.request.user.username))

                
                self.request.session['welcome_message_shown'] = True

        return response
    



@require_POST
def export_tasks(request):
    tasks = Task.objects.filter(created_by=request.user)
    tasks_data = []

    for task in tasks:
        task_data = {
            'title': task.title,
            'description': task.description,
            'created_at': task.created_at,
            'due_date': task.due_date,
            'completed_date': task.completed_date,
            'completed': task.completed,
            'user': task.created_by.username,
            'categories': ', '.join([category.name for category in task.categories.all()]),
            'tags': ', '.join([tag.name for tag in task.tags.all()]),
        }
        tasks_data.append(task_data)

    if 'export_csv' in request.POST:
        # Code d'exportation CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

        writer = csv.writer(response)
        writer.writerow(['Title', 'Description', 'Created At', 'Due_date', 'Completed Date', 'Completed', 'User', 'Categories', 'Tags'])

        for task_data in tasks_data:
            writer.writerow([
                task_data['title'],
                task_data['description'],
                task_data['created_at'],
                task_data['due_date'],
                task_data['completed_date'],
                task_data['completed'],
                task_data['user'],
                task_data['categories'],
                task_data['tags'],
            ])

        return response
    else:
        # Code d'exportation JSON
        return JsonResponse({'tasks': tasks_data}, json_dumps_params={'indent': 2})


# ...
# @csrf_protect

def update_category(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('create_category')  
    else:
        form = CategoryForm(instance=category)

    return render(request, 'tasks_app/update_category_form.html', {'update_category_form': form})
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        category.delete()
        return redirect('create_category')

    return render(request, 'tasks_app/delete_category.html', {'category': category})