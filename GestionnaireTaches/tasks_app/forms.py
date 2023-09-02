from django import forms
from .models import Task
from django.contrib.auth.forms import AuthenticationForm ,UserCreationForm
from django.contrib.auth.models import User

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.Textarea(attrs={'class': 'form-control'}),
                'completed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'role':'switch' ,'id': 'flexSwitchCheckDefault'}),

            }


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
