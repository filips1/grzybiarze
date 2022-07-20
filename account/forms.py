from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Moje_Konto


class RejestracjaForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Email jest wyamgany do założenia konta')

    class Meta:
        model = Moje_Konto
        fields = ("email", "username", "password1", "password2")


class LoginForm(forms.ModelForm):
    
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)

    class Meta:
        model = Moje_Konto
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username = username, password = password):
                raise forms.ValidationError("Podano błędne dane logowania")

class ZaktualizujKontoForm(forms.ModelForm):

    class Meta:
        model = Moje_Konto
        fields = ('email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Moje_Konto.objects.exclude(pk=self.instance.pk).get(email=email)
            except Moje_Konto.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s"jest już w użyciu' % email)

    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Moje_Konto.objects.exclude(pk=self.instance.pk).get(username=username)
            except Moje_Konto.DoesNotExist:
                return username
            raise forms.ValidationError('Email "%s"jest już w użyciu' % username)