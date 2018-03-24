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

           
LEVEL_CHOICES = (
    (0, 'blitz'),
    (1, 'low'),
    (2, 'medium'),
    (3, 'high'),
)

class MatchForm(forms.Form):
    level = forms.ChoiceField(label="Level", choices = LEVEL_CHOICES, initial=0)
    white_player_name = forms.CharField(label=' White Player', max_length=100)
    is_white_player_human = forms.BooleanField(label='Human', initial=True, required=False)
    black_player_name = forms.CharField(label='Black Player', max_length=100)
    is_black_player_human = forms.BooleanField(label='Human', initial=True, required=False)


    def clean(self):
        cleaned_data = super(MatchForm, self).clean()
        self.level = cleaned_data.get("level")
        self.white_player_name = cleaned_data.get("white_player_name")
        self.is_white_player_human = cleaned_data.get("is_white_player_human")
        self.black_player_name = cleaned_data.get("black_player_name")
        self.is_black_player_human = cleaned_data.get("is_black_player_human")

        if(not (len(self.white_player_name) > 0 and len(self.black_player_name) > 0)):
            raise ValidationError("...")


class ImportMatchForm(forms.Form):
    match_data = forms.CharField(label=' Put all data', max_length=4096)

    def clean(self):
        cleaned_data = super(ImportMatchForm, self).clean()
        self.match_data = cleaned_data.get("match_data")

