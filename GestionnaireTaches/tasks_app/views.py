from datetime import datetime
from .models import Task
from django.shortcuts import render, redirect
from django.urls import reverse,reverse_lazy

from django.views.generic import UpdateView, DeleteView
from django.views import View
from django.views.generic import ListView, CreateView

from .forms import TaskForm,CustomAuthenticationForm
from .forms import CustomUserCreationForm 

from django.core.paginator import Paginator
# from django.core.paginator import EmptyPage, PageNotAnInteger


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LogoutView,LoginView
# from django.contrib.auth.models import User

from django.http import JsonResponse
from django.db.models import Q




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
            due_date = datetime.strptime(due_date, '%Y-%m-%d')  # Convertir la chaîne en objet datetime

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
        # Créez un objet Paginator en utilisant self.object_list
        paginator = Paginator(self.object_list, self.paginate_by)
        
        # Obtenir le numéro de la page à partir des paramètres GET
        page_number = self.request.GET.get('page')
        # Obtenir la page courante
        page = paginator.get_page(page_number)

        context['page'] = page
        return context

   



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
    def form_valid(self, form):
        # Appeler la méthode parent pour effectuer la connexion
        response = super().form_valid(form)

        # Vérifier si l'utilisateur est authentifié (connecté)
        if self.request.user.is_authenticated:
            # Vérifier si le message de bienvenue a déjà été affiché
            if not self.request.session.get('welcome_message_shown', False):
                # Afficher le message de bienvenue
                messages.success(self.request, "Bienvenue, {} !".format(self.request.user.username))

                # Marquer le message comme affiché en définissant la session
                self.request.session['welcome_message_shown'] = True

        return response
    

