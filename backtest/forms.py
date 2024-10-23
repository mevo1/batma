from django import forms
from .models import Indicator

class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ['name', 'code', 'on_graph']

class MyForm(forms.Form):
    input_text = forms.CharField(label='Yazınız', max_length=100)
