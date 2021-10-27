import jwt
from django import forms
from django.conf import settings
from .models import HomeWorkManager


class HomeWorkManagerForm(forms.ModelForm):
    aiu_password = forms.CharField(label="Пароль от УИИ", max_length=500, widget=forms.PasswordInput)
    aiu_password2 = forms.CharField(label="Повторите пароль", max_length=500, widget=forms.PasswordInput)

    class Meta:
        model = HomeWorkManager
        fields = '__all__'

    def clean_aiu_password2(self):
        aiu_password = self.cleaned_data.get("aiu_password")
        aiu_password2 = self.cleaned_data.get("aiu_password2")
        if not aiu_password or not aiu_password2 or aiu_password != aiu_password2:
            raise forms.ValidationError("Passwords don't match")
        return aiu_password

    def save(self, commit=True):
        user = super(HomeWorkManagerForm, self).save(commit=False)
        user.aiu_password = jwt.encode({"password": user.aiu_password}, settings.SECRET_KEY).decode()
        if commit:
            user.save()
        return user