from django import forms
from .models import Transactions
from django.core.exceptions import ValidationError
import requests
from decouple import config 

class TransactionForm(forms.ModelForm):
    captcha = forms.CharField(required=True)

    class Meta:
        model = Transactions
        fields = ['book', 'amount', 'currency', 'stripe_token'] 

    def clean_captcha(self):
        captcha_response = self.cleaned_data.get('captcha')
        secret_key = config('RECAPTCHA_SECRET_KEY')
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={'secret': secret_key, 'response': captcha_response}
        )
        result = response.json()
        if not result.get('success'):
            raise ValidationError('Invalid CAPTCHA')
        return captcha_response
