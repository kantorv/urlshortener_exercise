from django.urls import path, include, re_path
from .views import create

urlpatterns = [
    re_path('^create$', create, name="create")
]
