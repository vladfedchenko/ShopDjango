from django.conf.urls import url

from . import views

app_name = 'shopapp'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^force/$', views.index_force, name='index_force'),
	url(r'^buy/(?P<obj_id>[0-9]+)/$', views.buy_item, name='buy_item'),
	url(r'^buy_confirm/$', views.buy_confirm, name='buy_confirm'),
	url(r'^leave_comment/(?P<obj_uid>[0-9]+)/$', views.leave_comment, name='leave_comment'),
	url(r'^(?P<category_val>[a-z]+)/(?P<page>[0-9]+)/$', views.category, name='category'),
	url(r'^(?P<category_val>[a-z]+)/item/(?P<obj_id>[0-9]+)/$', views.item_view, name='item_view'),
]
