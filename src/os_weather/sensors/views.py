import csv
import operator
import re
from collections import defaultdict
from datetime import datetime
from io import TextIOWrapper
import pytz

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView

from sensors.forms import LoaderForm, ChartForm
from sensors.models import ValuesModel, ValuesCalculatedModel


class LoaderView(FormView):
    template_name = 'sensors/loader.html'
    form_class = LoaderForm
    success_url = '/'
    date_pattern = '\d{8}'
    datetime_format = '%d%m%Y'

    def form_valid(self, form):
        daily = {}

        csv_by_date = self.__get_csv_by_dates(
            self.request.FILES.getlist('csv'))

        ordered_files_names = sorted(csv_by_date)

        sensor_data = self.__get_newest_values(ordered_files_names,
                                               csv_by_date)

        self.__dict_to_database(sensor_data)

        return super().form_valid(form)

    def __get_csv_by_dates(self, csv_list):
        # this function get the files ordered by date from oldest to newest

        pattern = re.compile(self.date_pattern)
        csv_by_date = {}

        for csv_file in csv_list:
            date_name = pattern.search(csv_file.name).group()
            datetime_object = datetime.strptime(date_name,
                                                self.datetime_format)
            csv_by_date[datetime_object] = csv_file

        return csv_by_date

    def __get_newest_values(self, ordered_files_names, csv_by_date):
        # Here we get a dictionary with the last values of the las file with
        # a datetime for sensor, how we have the files ordered by date, we
        # save at the end only the values from the most newest acquisition file

        sensor_data = defaultdict(lambda: defaultdict(
            lambda: defaultdict(lambda: defaultdict)))

        for index in ordered_files_names:
            csv_file = TextIOWrapper(csv_by_date[index])
            csv_data = csv.reader(csv_file, delimiter=",")

            sensor_name = csv_file.name.split('-')[0]
            # [signal, timestamp, value]
            for row in csv_data:
                sensor_data[sensor_name][row[0]][row[1]] = {
                    'value': int(row[2]),
                    'acquisition': index}

        return sensor_data

    def __dict_to_database(self, sensor_data):
        # This is neccesary to compare dates from database and dates from CSV
        time_zone = pytz.timezone(settings.TIME_ZONE)

        # We ommit the signals without calculation in our settings, maybe we can
        # create default calculation.
        #
        # We save first the values from csv to compare the csv value with
        # database value and get the most newest to can calculate the total of
        # each day.

        for sensor, sensor_value in sensor_data.items():
            for signal_name, calculation  in settings.CALCULATIONS.items():
                daily = defaultdict(list)
                for timestamp_key, dict_value in sensor_value[signal_name].items():
                    value = dict_value['value']
                    acquisition = dict_value['acquisition'].\
                        replace(tzinfo=time_zone)
                    timestamp = datetime.fromtimestamp(float(timestamp_key))

                    values_instance, created = ValuesModel.objects.get_or_create(
                            sensor=sensor,
                            signal=signal_name,
                            timestamp=timestamp_key
                    )

                    if created or (not created and values_instance.acquisition < acquisition):
                        values_instance.value = value
                        values_instance.acquisition = acquisition
                        values_instance.save()
                        daily[timestamp.date()].append(value)
                    else:
                        daily[timestamp.date()].append(values_instance.value)


                for day, values_list in daily.items():
                    values_calculated, created = ValuesCalculatedModel.objects.\
                        get_or_create(
                            sensor=sensor,
                            signal=signal_name,
                            day=day
                        )
                    values_calculated.value = calculation(values_list)
                    values_calculated.save()



class ChartsView(View):
    template_name="sensors/charts.html"
    form_class = ChartForm

    def get(self, request):
        context = {'form': self.form_class}
        return render(template_name=self.template_name,
                      context=context,
                      request=request)

    def post(self, request):
        form_fields = request.POST

        form_date_2_date = \
            lambda d, m, y: datetime.strptime('{}{}{}'.format(d, m, y),
                                              '%d%m%Y')

        start_date = form_date_2_date(form_fields['start_day_day'],
                                      form_fields['start_day_month'],
                                      form_fields['start_day_year'])

        end_date = form_date_2_date(form_fields['end_day_day'],
                                      form_fields['end_day_month'],
                                      form_fields['end_day_year'])

        signals = form_fields.getlist('signals')

        queryset = ValuesCalculatedModel.objects.filter(
            sensor=form_fields['sensor'],
            signal__in=signals,
            day__gt=start_date,
            day__lt=end_date
        )

        dict_data_chart = {}
        for signal in signals:
            data_by_date = defaultdict(int)

            for VCM in queryset.filter(signal=signal):
                granularity = settings.GRANULARITIES[form_fields['granularity']]
                data_by_date[granularity(VCM.day)] += VCM.value

            dict_data_chart[signal] = sorted(data_by_date.items(),
                                             key=operator.itemgetter(0))


        return JsonResponse(dict_data_chart)