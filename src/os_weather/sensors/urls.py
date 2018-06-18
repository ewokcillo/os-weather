from django.urls import path

from . import views

urlpatterns = [
    # Loader csv is the index of the application
    path('', views.LoaderView.as_view(), name='loader'),
]