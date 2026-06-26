from django import forms
from .models import Person
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class interoForm(forms.ModelForm):
  
       class Meta:
        model = Person
        fields = [ "date_of_birth","gender"]

class RegistrationForm(UserCreationForm):
       
       email =forms.EmailField(required=True)
       date_of_birth = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
       gender = forms.CharField(max_length=10)

       class Meta:
              model = User
              fields = ["email","username","password1","password2","date_of_birth", "gender"]
        