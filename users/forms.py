from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class NewRegisterForm(UserCreationForm):

    email=forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder':'Email','class':'input',}),label='')
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={'placeholder':'Username','class':'input'}),label='')
    password1=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'input'}),label='')
    password2=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password','class':'input'}),label='')
    class Meta:
        model=User
        fields=("username","email","password1","password2")

    def save(self,commit=True):
        user=super(NewRegisterForm,self).save(commit=False)
        user.email=self.cleaned_data['email']
        if commit:
            user.save()
        return user

