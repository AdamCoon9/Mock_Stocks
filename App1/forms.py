from django import forms
from .models import Stock

class TradeForm(forms.Form):
    stock = forms.ModelChoiceField(queryset=Stock.objects.all())
    shares = forms.IntegerField(min_value=1)
    action = forms.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])
