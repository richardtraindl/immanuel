from django import forms


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
