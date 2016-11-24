from django.conf.urls import url

from . import views

app_name = 'shopapp'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<category_val>[a-z]+)/(?P<page>[0-9]+)/$', views.category, name='category'),
]
