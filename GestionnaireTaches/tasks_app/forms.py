from django import forms
from .models import Task
from django.contrib.auth.forms import AuthenticationForm 

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
                'title': forms.TextInput(attrs={'class': 'form-control'}),
                'description': forms.Textarea(attrs={'class': 'form-control'}),
                'completed': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type': 'checkbox', 'role':'switch' ,'id': 'flexSwitchCheckDefault'}),

                # Ajoutez d'autres champs et leurs styles ici
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
