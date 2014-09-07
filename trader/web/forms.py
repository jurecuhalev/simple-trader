from django import forms
from django.core.exceptions import ValidationError

from web.models import TRADEORDER_QUALITY_CHOICES

class OrderAddForm(forms.Form):
    email = forms.EmailField()
    amount = forms.IntegerField()
    quality = forms.ChoiceField(choices=TRADEORDER_QUALITY_CHOICES)

    def clean_email(self):
        data = self.cleaned_data['email']
        if '@gmail.com' in data:
            raise ValidationError('We do not allow gmail.com email addresses')

        return data

    def clean_amount(self):
        data = self.cleaned_data['amount']

        if data < 1:
            raise ValidationError("Order amount must be more than 0")

        return data
