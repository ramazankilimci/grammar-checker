from django import forms

class SpellCheckForm(forms.Form):
    spell_text = forms.CharField(max_length=1000,
                                 widget=forms.Textarea
                                 )