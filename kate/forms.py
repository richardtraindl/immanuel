from django import forms


class DoMoveForm(forms.Form):
    move_src = forms.CharField(widget=forms.TextInput(attrs={'id':'move-src'}), label='move-src', id='move-src' max_length=3)
    move_dst = forms.CharField(widget=forms.TextInput(attrs={'id':'move-dst'}), label='move-dst', id='move-dst' max_length=3)
    prom_piece = forms.CharField(widget=forms.TextInput(attrs={'id':'prom-piece'}), label='prom-piece', id='prom-piece' max_length=3, initial="blk")
    switch = forms.IntegerField(widget=forms.TextInput(attrs={'id':'switch'}), label='switch', id='switch', initial=0)

    def clean(self):
        cleaned_data = super(DoMoveForm, self).clean()
        move_src = cleaned_data.get("move_src")
        move_dst = cleaned_data.get("move_dst")
        prom_piece = cleaned_data.get("prom_piece")
        switch = cleaned_data.get("switch")
