from django import forms

class SpellCheckForm(forms.Form):
    spell_text = forms.CharField(max_length=500,
                                 widget=forms.Textarea
                                 )