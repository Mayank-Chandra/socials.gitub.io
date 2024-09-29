from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'login_form',
        'placeholder':'Username'
    }))
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'login_form',
        'placeholder':'Password'
    }))    
    
class UserRegistrationForm(forms.ModelForm):
    password=forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2=forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput
    )
    
    class Meta:
        model=get_user_model()
        fields=['username','first_name','email']
        
    def cleaned_password2(self):
        cd=self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('Password does not match')
        return cd['password2']
    
    def clean_email(self):
       data=self.cleaned_data['email']
       qs=User.objects.exclude(
           id=self.instance.id
       ).filter(
           email=data
       )
       if qs.exists():
           raise forms.ValidationError('Email already in use.')
       return data
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model=get_user_model()
        fields=['first_name','last_name','email']
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['date_of_birth','photo']
