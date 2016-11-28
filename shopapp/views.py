from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import *
from datetime import datetime
from django.urls import reverse

categories = {'tv' : ('TVs', TV),
				'monitor' : ('Monitors', Monitor),
				'projector' : ('Projectors', Projector)}
				
rows = 4
cols = 4

def index(request):
	return render(request, 'shopapp/index.html')
	
def category(request, category_val, page):
	count = rows * cols
	page = int(page)
	start = (page - 1) * count
	finish = page * count
	cls = categories[category_val][1]
	
	obj_list = cls.objects.filter()[start:finish].all()
	
	context = {'objects' : obj_list,
				'rows' : range(rows),
				'cols' : range(cols),
				'cat_name' : category_val,}
	
	#tv = cls.objects.get(id=1)
	return render(request, 'shopapp/category.html', context)
	
def create_item_cell(obj, cat):
	template = loader.get_template('shopapp/item_cell.html')
	context = {'object' : obj,
			   'cat_name' : cat}
	return template.render(context)

def categories_list():
	template = loader.get_template('shopapp/categories.html')
	context = {'categories' : categories}
	return template.render(context)
	
def item_view(request, category_val, obj_id):
	cls = categories[category_val][1]
	obj = get_object_or_404(cls, pk=obj_id)
	context = {'obj' : obj}
	if (category_val == 'tv'):
		return render(request, 'shopapp/tv_view.html', context)
	elif (category_val == 'monitor'):
		return render(request, 'shopapp/monitor_view.html', context)
	elif (category_val == 'projector'):
		return render(request, 'shopapp/projector_view.html', context)
	else:
		raise Http404('Category does not exist')
		
def buy_item(request, obj_id):
	
	item = get_object_or_404(UniqueID, pk=obj_id)	
	cls = categories[item.item_type.name][1]
	obj = cls.objects.get(unique_id=item)
	
	#return HttpResponse(str(datetime.now()))
	
	user_item = UserItem(item=item
		, user=request.user
		, price=obj.price
		, date=datetime.now()
		, region=get_client_ip(request))
		
	user_item.save()
	return HttpResponseRedirect(reverse('shopapp:buy_confirm'))
	
def buy_confirm(request):
	return render(request, 'shopapp/item_bought.html')
	
def get_client_ip(request):
	x_f = request.META.get('HTTP_X_FORWARDED_FOR')
	if (x_f):
		ip = x_f.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return str(ip)
	
	
