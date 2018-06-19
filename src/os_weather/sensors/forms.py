from django import forms

from sensors.models import ValuesCalculatedModel as VCM


class LoaderForm(forms.Form):
    csv = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class ChartForm(forms.Form):
    GRANULARITY_CHOICES = (('daily', 'daily'),
                           ('weekly', 'weekly'),
                           ('monthly', 'monthly'))
    sensor = forms.CharField(widget=forms.Select())
    signals = forms.CharField(widget=forms.SelectMultiple)
    start_day = forms.DateField(widget=forms.SelectDateWidget())
    end_day = forms.DateField(widget=forms.SelectDateWidget())
    granularity = forms.CharField(
        widget=forms.Select(choices=GRANULARITY_CHOICES))

    def __init__(self, *args, **kwargs):
        super(ChartForm, self).__init__(*args, **kwargs)
        self.fields['sensor'] = forms.ChoiceField(
            choices=[(o['sensor'], o['sensor'])
                     for o in VCM.objects.values('sensor').distinct()])
        self.fields['signals'] = forms.ChoiceField(
            choices=[(o['signal'], o['signal'])
                     for o in VCM.objects.values('signal').distinct()])