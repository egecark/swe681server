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
         if not re.findall('^[a-zA-Z0-9!@-+]{6,}$', password): #check if findall is right one
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
    username = forms.RegexField(label=_("Username"), max_length=10, regex=r'^[\w.@+-_]{5,10}$',
        help_text = _("Required. 5 to 10 characters. Letters, digits and @/./+/-/_/' only."),
        error_messages = {'invalid': _("This value may contain only letters, numbers and @/./+/-/_/' characters and must be 5 to 10 charaters long.")})
    #maybe replace with EmailField
    email = forms.RegexField(label=_("Email"), max_length=25, regex=r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',
        help_text = _("Required. email address"),
        error_messages = {'invalid': _("Needs valid email address")})
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput) #does this need max length?
    password2 = forms.CharField(label=_("Password confirmation"), widget=forms.PasswordInput,
        help_text = _("Enter the same password as above, for verification."))


    class Meta:
        model = User
        fields = ("username",)

    #maybe clean email if we don't want multiple accounts per email

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

#class RegistrationForm(forms.ModelForm):
#    """
#    A form that creates a user, with no privileges, from the given username and
#    password.
#    """
#    error_messages = {
#        'password_mismatch': _('The two password fields didn’t match.'),
#    }
#    password1 = forms.CharField(
#        label=_("Password"),
#        strip=False,
#        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#        help_text=(PasswordValidator.get_help_text),
#    )
#    password2 = forms.CharField(
#        label=_("Password confirmation"),
#        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#        strip=False,
#        help_text=_("Enter the same password as before, for verification."),
#    )
#    username = forms.CharField(
#        label=_("Username"),
#        strip=False,
#        widget=forms.UsernameInput(attrs={'autocomplete': 'new-password'}),
#        help_text=(PasswordValidator.get_help_text),
#    )
#
#    class Meta:
#        model = User
#        fields = ("username",)
#        field_classes = {'username': UsernameField}
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        if self._meta.model.USERNAME_FIELD in self.fields:
#            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True
#
#    def clean_username(self):
#        username = self.cleaned_data['username']
#
#        if not re.findall('^[a-zA-Z0-9_-\']{5,15}$', username): #check if findall is right one
#            raise ValidationError(
#                _("The username must be 5-15 digits with alphanumeric characters, apostrophe, underscores, or dashes"),
#                code='username',
#            )
#
#
#    def clean_password2(self):
#        password1 = self.cleaned_data.get("password1")
#        password2 = self.cleaned_data.get("password2")
#        if password1 and password2 and password1 != password2:
#            raise ValidationError(
#                self.error_messages['password_mismatch'],
#                code='password_mismatch',
#            )
#        return password2
#
#    def _post_clean(self):
#        super()._post_clean()
#        # Validate the password after self.instance is updated with form data
#        # by super().
#        password = self.cleaned_data.get('password2')
#        if password:
#            try:
#                PasswordValidator(password, self.instance)
#            except ValidationError as error:
#                self.add_error('password2', error)
#
#    def save(self, commit=True):
#        user = super().save(commit=False)
#        user.set_password(self.cleaned_data["password1"])
#        if commit:
#            user.save()
#        return user
