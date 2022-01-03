from django import forms
from django.utils.html import format_html

class dichotomyForm(forms.Form):

    choices = [('SI/NO','SI/NO'),('A favor/En contra','A favor/En contra'),('Verdadero/Falso','Verdadero/Falso'),('Bien/Mal','Bien/Mal')]
    question_desc = forms.CharField(label="Escriba una pregunta", widget=forms.Textarea, required=True)
    question_ratio = forms.ChoiceField(label=format_html("<br><br>{} ","Seleccione el tipo respuesta  "), widget=forms.RadioSelect, required=True,choices=choices)

class chooseTypeForm(forms.Form):
    choices = [('m','Pregunta multielección'),('d','Pregunta dicotómica')]
    type_ratio = forms.ChoiceField(label="Tipo:", widget=forms.RadioSelect, required=True,choices=choices)

def clean_url(self):
    url = self.cleaned_data.get['url']
    if url == '/':
        raise forms.ValidationError('El valor / no es válido')
    return url