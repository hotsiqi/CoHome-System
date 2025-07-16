from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import HouseUnit, HouseImage, MALAYSIA_STATE_CHOICES,Contract,TechnicianReport ,HOUSE_TYPE_CHOICES, BEDROOM_CHOICES,Profile ,PaymentProof




class OwnerRegisterForm(UserCreationForm):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=255, help_text='Required.')
    bank_account_number = forms.CharField(max_length=20, required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'bank_account_number', 'password1', 'password2']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'bank_account_number']


class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = PaymentProof
        fields = ['proof']


class SearcherRegisterForm(UserCreationForm):
    email = forms.EmailField()
    full_name = forms.CharField(max_length=255, help_text='Required.')

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'password1', 'password2']



class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class HouseUnitForm(forms.ModelForm):
    location = forms.ChoiceField(choices=MALAYSIA_STATE_CHOICES)
    house_type = forms.ChoiceField(choices=HOUSE_TYPE_CHOICES)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = forms.ChoiceField(choices=BEDROOM_CHOICES)

    class Meta:
        model = HouseUnit
        fields = ['description', 'location', 'house_type', 'price', 'bedrooms']

HouseImageFormSet = inlineformset_factory(
    HouseUnit, HouseImage,
    fields=['image',],
    extra=3,  
    can_delete=True

)

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        exclude = ('uploaded_by',)
        fields = ['house_unit', 'contract_file']
        widgets = {
            'house_unit': forms.HiddenInput(),
        }

class TechnicianReportForm(forms.ModelForm):
    class Meta:
        model = TechnicianReport
        fields = ['title', 'description', 'photo']


class HouseUnitSearchForm(forms.Form):
    description = forms.CharField(required=False)
    house_type = forms.ChoiceField(choices=HOUSE_TYPE_CHOICES, required=False)
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)