from django import forms
from .models import Indicator, Strategy


class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ['name', 'code', 'on_graph']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        user = self.initial['user']  # Mevcut kullanıcıyı alıyoruz
        
        # Aynı isimde ve aynı kullanıcıya ait bir indikatör olup olmadığını kontrol et
        if Indicator.objects.filter(name=name, user=user).exists():
            raise forms.ValidationError(f"'{name}' isminde bir indikatör zaten var.")
        
        return name

class MyForm(forms.Form):
    input_text = forms.CharField(label='Yazınız', max_length=100)

