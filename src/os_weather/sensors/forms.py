from django import forms

class LoaderForm(forms.Form):
    csv = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
