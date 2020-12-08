from django import forms
from django.contrib.auth.forms import *
import re
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
#from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
User = get_user_model()

#Needs actual regex for password and username
class PasswordValidator(object):
    def validate(self, password, user=None):
         if not re.findall('^[a-zA-Z0-9!@\-\+]{6,50}$', password):
            raise ValidationError(
                _("The password must contain at least 6 characters, alphanumeric or !/@/-/+, ."),
                code='password',
            )

    def get_help_text(self):
        return _(
            "The password must contain at least 6 alphanumeric characters."
        )

class RegistrationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """
    #need to add ' into username
    username = forms.RegexField(label=_("Username"), max_length=10, regex=r'^[\w\.@\+\-_\']{5,10}$',
        help_text = _("Required. 5 to 10 characters. Letters, digits and @/./+/-/_/' only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_/' characters and must be 5 to 10 charaters long.")})
    email = forms.RegexField(label=_("Email"), max_length=50, regex=r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
        help_text = _("Required. email address"),
        error_messages = {'invalid': _("Needs valid email address")})
    password1 = forms.RegexField(label=_("Password"), max_length=50, regex=r'^[a-zA-Z0-9!@\-\+]{6,50}$', widget=forms.PasswordInput)
    password2 = forms.RegexField(label=_("Password confirmation"), max_length=50, regex=r'^[a-zA-Z0-9!@\-\+]{6,50}$', widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))


    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

