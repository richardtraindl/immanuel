from django import forms
from .models import LEVELS


class DoMoveForm(forms.Form):
    move_src = forms.CharField(widget=forms.TextInput(attrs={'id':'move-src'}), label='move-src', max_length=3)
    move_dst = forms.CharField(widget=forms.TextInput(attrs={'id':'move-dst'}), label='move-dst', max_length=3)
    prom_piece = forms.CharField(widget=forms.TextInput(attrs={'id':'prom-piece'}), label='prom-piece', max_length=3, initial="blk")

    def clean(self):
        cleaned_data = super(DoMoveForm, self).clean()
        move_src = cleaned_data.get("move_src")
        move_dst = cleaned_data.get("move_dst")
        prom_piece = cleaned_data.get("prom_piece")

        if(not (len(move_src) > 0 and len(move_dst) > 0 and len(prom_piece) > 0) ):
            raise ValidationError("...")


class MatchForm(forms.Form):
    white_player = forms.CharField(label=' White Player', max_length=100)
    white_player_human = forms.BooleanField(label='Human', initial=True)
    black_player = forms.CharField(label='Black Player', max_length=100)
    black_player_human = forms.BooleanField(label='Human', initial=True)
    level = models.IntegerField(label='Level', choices=LEVELS, default=1)

    def clean(self):
        cleaned_data = super(MatchForm, self).clean()
        white_player = cleaned_data.get("white_player")
        white_player_human = cleaned_data.get("white_player_human")
        black_player = cleaned_data.get("black_player")
        black_player_human = cleaned_data.get("black_player_human")
        level = cleaned_data.get("level")

        if(not (len(white_player) > 0 and len(black_player) > 0)):
            raise ValidationError("...")

