from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Mi nombre es', max_length=100)