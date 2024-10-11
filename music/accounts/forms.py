from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm



#regitration

class CreateUserForm(UserCreationForm):
   password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password',                                            'class':'form-control',
                                         'style':'max-width:600px;  '}))
   password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password',                                            'class':'form-control',
                                         'style':'max-width:600px;  '}))
   class Meta:
        model = Customer
        fields = ['username', 'email','password1', 'password2']
        widgets = { 
            'username': forms.TextInput(attrs=
                                        {'placeholder': 'First Name',
                                         'class':'form-control',
                                         'style':'max-width:600px; '
                                         
                                         }),
            'email': forms.TextInput(attrs={'placeholder': 'Email',
                                            'class':'form-control',
                                         'style':'max-width:600px;  '}),
            
             }  
        
        