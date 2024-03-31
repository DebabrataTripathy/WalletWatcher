from django import forms
from.models import Expense
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'
class InputForm(forms.ModelForm):

    class Meta:
        model=Expense
        fields=['name','price','category','date']
        widgets = {
            'date': DateInput(),
        }


class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','first_name','last_name','password']
