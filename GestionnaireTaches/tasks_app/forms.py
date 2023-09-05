from django import forms
from .models import Category, Task 
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm
from django.contrib.auth.models import User
# from django.forms.widgets import Select
from django.forms import inlineformset_factory
from taggit.forms import TagWidget


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,  # Rendre le champ facultatif
        widget=forms.DateInput(attrs={'type': 'date'}),  
    # categories = forms.ModelChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     required=False,  # Vous pouvez définir ceci comme True si une catégorie est obligatoire
    )
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.Textarea(attrs={'class': 'form-control'}),
                'completed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'role':'switch' ,'id': 'flexSwitchCheckDefault'}),
                'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
                'tags': TagWidget(attrs={'class': 'form-control'}),
            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].required = False

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        help_text='Required. Your password.'
    )
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  
        fields = ['username', 'password1', 'password2']  

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True,
        help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        help_text='Required. Your password.'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        help_text='Enter the same password as before, for verification.'
    )
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

# class TagForm(forms.Form):
#     # Définissez les champs du formulaire Tag ici
#     name = forms.CharField(max_length=255)
#     color = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'type': 'color'}))
        