from django import forms


class DoMoveForm(forms.Form):
    move_src = forms.CharField(widget=forms.TextInput(attrs={'id':'move-src'}), label='move-src', max_length=3)
    move_dst = forms.CharField(widget=forms.TextInput(attrs={'id':'move-dst'}), label='move-dst', max_length=3)
    prom_piece = forms.CharField(widget=forms.TextInput(attrs={'id':'prom-piece'}), label='prom-piece', max_length=3, initial="blk")

    def clean(self):
        cleaned_data = super(DoMoveForm, self).clean()
        self.move_src = cleaned_data.get("move_src")
        self.move_dst = cleaned_data.get("move_dst")
        self.prom_piece = cleaned_data.get("prom_piece")

        if(not (len(self.move_src) > 0 and len(self.move_dst) > 0 and len(self.prom_piece) > 0) ):
            raise ValidationError("...")

           
LEVELS = (
    ('0', 'blitz'),
    ('1', 'low'),
    ('2', 'medium'),
    ('3', 'high'),
)

class MatchForm(forms.Form):
    white_player = forms.CharField(label=' White Player', max_length=100)
    white_player_human = forms.BooleanField(label='Human', initial=True, required=False)
    black_player = forms.CharField(label='Black Player', max_length=100)
    black_player_human = forms.BooleanField(label='Human', initial=True, required=False)
    level = forms.ChoiceField(label="Level", choices = LEVELS, initial='0')

    def clean(self):
        cleaned_data = super(MatchForm, self).clean()
        self.white_player = cleaned_data.get("white_player")
        self.white_player_human = cleaned_data.get("white_player_human")
        self.black_player = cleaned_data.get("black_player")
        self.black_player_human = cleaned_data.get("black_player_human")
        self.level = cleaned_data.get("level")

        if(not (len(self.white_player) > 0 and len(self.black_player) > 0)):
            raise ValidationError("...")

