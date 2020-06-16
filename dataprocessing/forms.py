
from django import forms 

from .models import userinput
from django.forms import ModelForm, TextInput

class userinput(forms.ModelForm): 
    class Meta: 
        model = userinput 
        fields = "__all__"