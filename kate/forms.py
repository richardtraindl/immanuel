from django import forms


classDoMoveForm(forms.Form):
    move_src = forms.CharField(label='move-src', id='move-src' max_length=3)
    move_dst = forms.CharField(label='move-dst', id='move-dst' max_length=3)
    prom_piece = forms.CharField(label='prom-piece', id='prom-piece' max_length=3)
    switch = forms.CharField(label='switch', id='switch' max_length=3)

   
