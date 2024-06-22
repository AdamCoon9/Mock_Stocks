from django import forms
from .models import Stock, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class TradeForm(forms.Form):
    stock = forms.ModelChoiceField(queryset=Stock.objects.all())
    shares = forms.IntegerField(min_value=1)
    action = forms.ChoiceField(choices=[('buy', 'Buy'), ('sell', 'Sell')])

class BuyStockForm(forms.Form):
    stock = forms.ModelChoiceField(queryset=Stock.objects.all())
    quantity = forms.IntegerField(min_value=1, label='Quantity')

class SellStockForm(forms.Form):
    stock = forms.ModelChoiceField(queryset=Stock.objects.none())  # We will set queryset in the view
    quantity = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(SellStockForm, self).__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(portfolio__user=self.user)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']
    def save(self, user=None, commit=True):
        profile = super(UserProfileForm, self).save(commit=False)
        if user:
            profile.user = user

        if commit:
            profile.save()

        return profile



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    balance = forms.DecimalField(max_digits=10, decimal_places=2, max_value=10000)  # Balance field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'balance']  # Include balance in the fields
