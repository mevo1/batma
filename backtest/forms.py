from django import forms

class MyForm(forms.Form):
    input_text = forms.CharField(label='Yazınız', max_length=100)
