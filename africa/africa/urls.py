from django.contrib import admin
from django.urls import path, include
from django.urls import re_path as url

from API.views.views import GetStoveInfoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GetStoveInfoView.as_view(), name='on_shit')
]
