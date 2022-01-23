from django.urls import path, include, re_path
from .views import create, redirect_view

urlpatterns = [
    re_path('^create$', create, name="create"),
    re_path(r'^s/(?P<hash>[A-Za-z0-9]{7})$', redirect_view),
]
