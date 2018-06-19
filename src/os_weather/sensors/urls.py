from django.urls import path

from . import views

urlpatterns = [
    path('charts', views.ChartsView.as_view(), name='charts'),
    # Loader csv is the index of the application
    path('', views.LoaderView.as_view(), name='loader'),
]