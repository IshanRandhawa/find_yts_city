
from django import forms 

from .models import userinput
from django.forms import ModelForm

class userinput(forms.ModelForm): 
    class Meta: 
        model = userinput 
        fields = ('query','city','number_queries')
    
        widgets = {
            'query': forms.TextInput(attrs={'class': 'styles.css' , 'placeholder':'Your interests'}),
            'city': forms.Select(attrs={'class': 'styles.css',  'placeholder':'Choose a city from the list'}),
            'number_queries':forms.NumberInput(attrs={'class': 'styles.css', 'type':'range','min':"1", 'max':"50" ,'onchange':"updateTextInput(this.value)"}),
        }
        labels = {
            "number_queries": "Number of results",
        }
        # help_texts = {
        #     'query': ('Type what type of youtubers you are looking for'),
        # }
