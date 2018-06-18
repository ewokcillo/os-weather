from django.shortcuts import render
from django.views.generic.edit import FormView

from sensors.forms import LoaderForm


class LoaderView(FormView):
    template_name = 'sensors/loader.html'
    form_class = LoaderForm
    success_url = '/'

    def form_valid(self, form):
        csv_files = self.request.FILES


        return super().form_valid(form)