from django.conf.urls import url
from . import views

# dispatch URLS here
app_name = 'visualize'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^(?P<simulation_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<simulation_id>[0-9]+)/params/$', views.params , name='params'),
]
