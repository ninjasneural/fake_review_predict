from django.conf.urls import url
from reviewpost import views

urlpatterns=[
    url('review/',views.review),
    url('history/',views.history),
]