
from django import forms 

from .models import userinput


class userinput(forms.ModelForm): 
    class Meta: 
        model = userinput 
        fields = "__all__"