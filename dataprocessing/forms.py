
from django import forms 

from .models import userinput
from django.forms import ModelForm

class userinput(forms.ModelForm): 
    class Meta: 
        model = userinput 
        fields = ('query','city','number_queries')
    
        widgets = {
            'query': forms.TextInput(attrs={'class': 'form-control' , 'placeholder':'Your interests'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'number_queries':forms.NumberInput(attrs={'class': 'form-control', 'type':'range','min':"1", 'max':"50" ,'onchange':"updateTextInput(this.value)"}),
        }

        # help_texts = {
        #     'query': ('Type what type of youtubers you are looking for'),
        # }
