# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django import forms

from .models import VomUser


class UserForm(forms.ModelForm):
    error_messages = {
        'invalid': _(
            "You must choice 1 or 0. 1 means male, 0 means female."
        ),
        'password_mismatch': _("The two password fields didn't match."),
    }

    password2 = forms.CharField()

    class Meta:
        model = VomUser
        fields = ('email', 'name', 'birthday', 'sex', 'password',)

    def clean_sex(self):
        if self.cleaned_data.get('sex') not in (0, 1):
            raise forms.ValidationError(
                self.error_messages['invalid'],
                code='invalid',
            )
        return self.cleaned_data['sex']

    def clean_password2(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data.get('password')
            password2 = self.cleaned_data.get('password2')
            if password == password2:
                return password2
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password2"))
        if commit:
            user.save()
        return user
