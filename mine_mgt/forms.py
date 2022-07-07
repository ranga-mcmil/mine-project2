from django import forms
from .models import Proof, Claim, Payment

class ProofForm(forms.ModelForm):

    class Meta:
        model = Proof
        fields = ('image',)


class ClaimForm(forms.ModelForm):
    location = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Harare, Zimbabwe',
        }
    ))

    address = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '21 Hillcrest Rd',
        }
    ))

    size_approximation = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '300Ha',
        }
    ))



    class Meta:
        model = Claim
        fields = ('location', 'address', 'size_approximation')



class PaymentForm(forms.ModelForm):
    amount = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': '230',
        }
    ))

    reason = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Monthly Payment',
        }
    ))

    class Meta:
        model = Payment
        fields = ('amount', 'reason')