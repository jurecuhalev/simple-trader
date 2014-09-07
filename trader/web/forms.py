from django import forms

from web.models import TRADEORDER_QUALITY_CHOICES

class OrderAddForm(forms.Form):
	email = forms.EmailField()
	amount = forms.IntegerField()
	quality = forms.ChoiceField(choices=TRADEORDER_QUALITY_CHOICES)