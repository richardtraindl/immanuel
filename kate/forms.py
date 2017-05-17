from django import forms


class DoMoveForm(forms.Form):
    move_src = forms.CharField(widget=forms.TextInput(attrs={'id':'move-src'}), label='move-src', id='move-src' max_length=3)
    move_dst = forms.CharField(widget=forms.TextInput(attrs={'id':'move-dst'}), label='move-dst', id='move-dst' max_length=3)
    prom_piece = forms.CharField(widget=forms.TextInput(attrs={'id':'prom-piece'}), label='prom-piece', id='prom-piece' max_length=3)
    switch = forms.IntegerField(widget=forms.TextInput(attrs={'id':'switch'}), label='switch', id='switch')

   
