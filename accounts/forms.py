from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    face_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class FaceLoginForm(forms.Form):
    face_image = forms.ImageField()
