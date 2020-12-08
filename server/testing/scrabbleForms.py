from django.forms import ModelForm
from django import forms
from . import models
from .models import *
from django.utils.translation import ugettext as _

word_regex = r'^(([A-Za-z](,([0-9]|[1][0-4])){2}),){0,6}[A-Za-z](,([0-9]|[1][0-4])){2}$'

class WordForm(forms.Form):


    #This checks for a uuid, but not specific to a uuid4
    id = forms.RegexField(label=_("Game id"), max_length=36, regex=r'^[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}$',
                            help_text = _("Insert game id here"),
                            error_messages = {'invalid': _("Invalid game id.")})


    #^[A-Za-z](,([1-9]|[1][0-5])){2}$
    word = forms.RegexField(label=_("Input Word"), max_length=56, regex=word_regex,
                            help_text = _("Input word of the form: letter-row-col"),
                            error_messages = {'invalid': _("Invalid move.")})

#    def clean_id(self):
#        id = self.cleaned_data["id"]
##        if condition:
##            raise forms.ValidationError(_("Invalid id."))
#        return id
#
    def clean_word(self):
        word = self.cleaned_data["word"]
        return word.capitalize()
##        if condition:
##            raise forms.ValidationError(_("Invalid move."))

    def save(self):
        data = self.cleaned_data

        word = Word(id=data['id'], word=data['word'])
        word.save()

        return word

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

    #This checks for a uuid, but not specific to a uuid4
    id = forms.RegexField(label=_("Game id"), max_length=36, regex=r'^[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}$',
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
