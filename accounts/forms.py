from django import forms
from .models import Profile, Address
from django.contrib.auth import get_user_model
User = get_user_model()
class ProfileEditForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30 , required=False)
    email = forms.EmailField(required=False)

class PasswordReset(forms.Form):
    old_password = forms.CharField(max_length=18)
    new_password = forms.CharField(max_length=18)
    help_text = 'password should have atleast 6 characters'

class AddressEditForm(forms.ModelForm):
    class Meta:
        model= Address
        fields = ['full_name','county','phone_no','address']
