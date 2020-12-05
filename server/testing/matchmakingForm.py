from django.forms import ModelForm
from django import forms
from . import models
from .models import *
from django.utils.translation import ugettext as _

class MatchMakingHostingForm(ModelForm):
    class Meta:
        model = Matchmaking
        fields = ['num_players']

    #if number of players not between 2 and 4, send validation error
    def clean_num_players(self):
        num_players = self.cleaned_data["num_players"]
        if num_players > 4 or num_players < 2:
            raise forms.ValidationError(_("Invalid number of players. Should be between 2 and 4."))
        return num_players

class MatchMakingJoiningForm(forms.Form):
#    class Meta:
#        model = Matchmaking
#        fields = ['id']
#        widget = {'id' : forms.RegexField(label=_("Game id"), max_length=10, regex=r'^[0-9]{1,10}&$',
#                   help_text = _("1 to 10 digit game id"),
#                   error_messages = {'invalid': _("This field may contain up to 10 digits.")})
#                 }

    id = forms.RegexField(label=_("Game id"), max_length=50, regex=r'^[a-z0-9\-]{1,50}$',
                            help_text = _("Insert game id here"),
                            error_messages = {'invalid': _("Invalid game id.")})

    #if matchmaking id does not exist, validation error
    def clean_id(self):
        id = self.cleaned_data["id"]
        try:
            Matchmaking.objects.get(id=id)
        except Matchmaking.DoesNotExist:
            raise forms.ValidationError(_("Cannot join requested match."))
        return id

#not sure how we want to clean client ids yet
'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client1_match', default=None, on_delete=models.CASCADE)
    client2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client2_match', default=None, null=True, on_delete=models.CASCADE)
    client3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client3_match', default=None, null=True, on_delete=models.CASCADE)
    client4 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client4_match', default=None, null=True, on_delete=models.CASCADE)
    num_players = models.PositiveIntegerField(default=0)
'''

