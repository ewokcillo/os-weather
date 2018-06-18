from django.db import models

# Create your models here.

class SensorBaseModel(models.Model):
    sensor = models.CharField(max_length=64)
    signal = models.CharField(max_length=64)
    value = models.FloatField(blank=True, null=True)

    class Meta:
        abstract = True


class ValuesModel(SensorBaseModel):
    #Model to save each row from CSV's in databasa
    timestamp = models.CharField(max_length=10)
    acquisition = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('sensor', 'signal', 'timestamp')


class ValuesCalculatedModel(SensorBaseModel):
    # Model to save the daily calculation of each load CSV's
    day = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('sensor', 'signal', 'day')