from django.forms import ModelForm
from . import models

class GameForm(ModelForm):
    class Meta:
        model = models.GameState


#not sure where to validate client 
#    def clean_client1(self):
#        client1 = self.cleaned_data["client1"]
#        try:
#            User.objects.get(username=username)
#        except User.DoesNotExist:
#            return username
#        raise forms.ValidationError(_("A user with that username already exists."))

#User probably shouldn't send board?
#    def clean_board(self):
#        board = self.cleaned_data["board"]

        


'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    turn = models.CharField(max_length=20, default='game_not_started')
    board = models.CharField(max_length=5000)
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='start_time')
    client1 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client1_game', default=None, on_delete=models.CASCADE)
    client2 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client2_game', default=None, on_delete=models.CASCADE)
    client3 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client3_game', default=None, null= True, on_delete=models.CASCADE)
    client4 = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='client4_game', default=None, null= True, on_delete=models.CASCADE)
    score_1 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)
    score_3 = models.IntegerField(null=True, default=None)
    score_4 = models.IntegerField(null=True, default=None)
'''
