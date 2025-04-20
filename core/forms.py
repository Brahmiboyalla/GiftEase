from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Payment, SalePayment, User
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, GiftCard, Transaction, PaymentMethod
from django.core.validators import RegexValidator


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'contact', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'contact']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
        }


class GiftCardForm(forms.ModelForm):
    class Meta:
        model = GiftCard
        fields = ['brand', 'background_image', 'value', 'buy_back_price']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),
            'background_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
            'buy_back_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Buy Back Price'}),
        }

GIFT_CARD_RULES = {
    "Amazon":     {"prefixes": ["AMZ", "AQ"],   "lengths": [14, 16]},
    "Flipkart":   {"prefixes": ["FLPK", "FK"],  "lengths": [16]},
    "Myntra":     {"prefixes": ["MYN"],         "lengths": [12, 16]},
    "Walmart":    {"prefixes": ["WMT", "WAL"],  "lengths": [16]},
    "Target":     {"prefixes": ["TGT", "TRG"],  "lengths": [15, 16]},
    "eBay":       {"prefixes": ["EBY", "EB"],   "lengths": [13, 16]},
    "Starbucks":  {"prefixes": ["SBX", "SB"],   "lengths": [14, 16]},
}

def is_valid_gift_card(brand, card_number):
    rules = GIFT_CARD_RULES.get(brand)
    if not rules:
        return False
    prefix_match = any(card_number.startswith(prefix) for prefix in rules["prefixes"])
    length_match = len(card_number.replace("-", "")) in rules["lengths"]
    return prefix_match and length_match

class TransactionForm(forms.ModelForm):
    card_number = forms.CharField(
        max_length=19,  # Includes hyphens
        validators=[RegexValidator(r'^[A-Za-z0-9-]{12,19}$', 'Enter a valid card number (12-19 characters, alphanumeric + hyphens).')],
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}),
    )

    class Meta:
        model = Transaction
        fields = ['brand','card_number', 'card_holder', 'expiry_date', 'pin', 'amount']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control','readonly': True}),
            'card_holder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Holder Name'}),
            'expiry_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}),
            'pin': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'PIN', 'maxlength': '4'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Transaction Amount'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        brand = cleaned_data.get("brand")
        card_number = cleaned_data.get("card_number")

        if brand and card_number:
            if not is_valid_gift_card(brand, card_number):
                raise ValidationError("Card number doesn't match the format expected for the selected brand.")

class ReceivePaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['account_number', 'bank_name', 'ifsc_code', 'account_holder', 'amount']
        widgets = {
            'account_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Account Number'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Name'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IFSC Code'}),
            'account_holder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Holder Name'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
        }

class SalePaymentForm(forms.ModelForm):
    amount = forms.DecimalField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = SalePayment
        fields = ['method', 'amount']
        widgets = {
            'method': forms.Select(attrs={'class': 'form-control', 'onchange': 'toggleWalletField()'}),
            'amount': forms.HiddenInput(),  # ✅ Hides the field
        }
    def __init__(self, *args, **kwargs):
        super(SalePaymentForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs and 'amount' in kwargs['initial']:
            self.fields['amount'].initial = kwargs['initial']['amount']

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['method', 'upi_id', 'card_number', 'card_holder_name', 'expiry_date', 'account_number', 'bank_name', 'ifsc_code']
        widgets = {
            'method': forms.Select(attrs={'class': 'form-control', 'onchange': 'toggleFields()'}),
            'upi_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter UPI ID'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}),
            'card_holder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cardholder Name'}),
            'expiry_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'}),
            'account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Account Number'}),
            'bank_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bank Name'}),
            'ifsc_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IFSC Code'}),
        }