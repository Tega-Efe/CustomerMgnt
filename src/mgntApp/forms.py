from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm ,UsernameField ,PasswordChangeForm,SetPasswordForm,PasswordResetForm

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']


class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class createCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
     
		
# class createOrderForm(ModelForm):
# 	class Meta:
# 		model = Order
# 		fields = '__all__'



class createOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the logged-in user
        super().__init__(*args, **kwargs)
        if user:
            self.fields['customer'].disabled = True  # Make customer field read-only
            self.fields['customer'].initial = user.customer # Set initial value to username of logged-in user




class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'# Add other fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].disabled = True  # Make customer field read-only

    def clean_customer(self):
        return self.instance.customer  # Ensure the customer field value is not changed during form submission


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email','password1','password2']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label = 'Old Password', widget=forms.PasswordInput(attrs={'autofocus':True,'autocomplete':'current-password','class':'form-control'}))
    new_password1 = forms.CharField(label = 'New Password', widget=forms.PasswordInput(attrs={'autofocus':True,'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput(attrs={'autofocus':True,'autocomplete':'current-password','class':'form-control'}))


class MyPasswordresetForm(PasswordResetForm):
   email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label = 'New Password', widget=forms.PasswordInput(attrs=
    {'autofocus':True,'autocomplete':'current-password','class':'form-control'}))
    new_password2 = forms.CharField(label = 'Confirm New Password', widget=forms.PasswordInput(attrs=
    {'autofocus':True,'autocomplete':'current-password','class':'form-control'}))