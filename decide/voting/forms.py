from django import forms


class YesOrNotForm(forms.Form):
    question_desc = forms.CharField(label="Escriba una pregunta", widget=forms.TextInput, required=True)
