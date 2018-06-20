from datetime import datetime

from django import forms
from django.conf import settings

from sensors.models import ValuesCalculatedModel as VCM


class LoaderForm(forms.Form):
    csv = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class ChartForm(forms.Form):
    GRANULARITY_CHOICES = (
        (key, key) for key in settings.GRANULARITIES.keys())
    YEARS = list(range(datetime.now().year - 9,
                       datetime.now().year + 9))

    sensor = forms.CharField(widget=forms.Select())
    signals = forms.MultipleChoiceField(widget=forms.SelectMultiple())
    start_day = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
    end_day = forms.DateField(widget=forms.SelectDateWidget(years=YEARS))
    granularity = forms.CharField(
        widget=forms.Select(choices=GRANULARITY_CHOICES))

    def __init__(self, *args, **kwargs):
        super(ChartForm, self).__init__(*args, **kwargs)
        self.fields['sensor'] = forms.ChoiceField(
            choices=[(o['sensor'], o['sensor'])
                     for o in VCM.objects.values('sensor').distinct()])
        self.fields['signals'] = forms.MultipleChoiceField(
            choices=[(o['signal'], o['signal'])
                     for o in VCM.objects.values('signal').distinct()])