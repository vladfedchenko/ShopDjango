from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import *
from datetime import datetime
from django.urls import reverse
import sys

categories = {'tv' : ('TVs', TV),
				'monitor' : ('Monitors', Monitor),
				'projector' : ('Projectors', Projector)}
				
rows = 4
cols = 4

def index(request):
	return render(request, 'shopapp/index.html')
	
def category(request, category_val, page):
	count = rows * cols
	
	if request.POST.get('action_button'):
		act = request.POST.get('action_button')
		if (act == '< Prev'):
			page = int(page) - 1
		elif (act == 'Next >'):
			page = int(page) + 1
		else:
			page = 1
			
	else:
		page = 1
	start = (page - 1) * count
	finish = page * count
	cls = categories[category_val][1]
	
	obj_list, filt = filter_objects(request, cls.objects)
	
	obj_count = obj_list.count()
	
	can_go_next = obj_count >= finish
	
	obj_list = obj_list.filter()[start:finish].all()
	
	can_go_prev = page != 1
	
	context = {'objects' : obj_list,
				'rows' : range(rows),
				'cols' : range(cols),
				'cat_name' : category_val,
				'filter' : filt,
				'cur_page' : page,
				'can_go_prev' : can_go_prev,
				'can_go_next' : can_go_next,
				}
	
	#tv = cls.objects.get(id=1)
	return render(request, 'shopapp/category.html', context)
	
def filter_objects(request, obj_set):
	
	filt = {}
	if request.POST.get('min_price'):
		tmp = float(request.POST.get('min_price'))
		obj_set = obj_set.filter(price__gte=tmp)
		filt['min_price'] = tmp
	
	if request.POST.get('max_price'):
		tmp = float(request.POST.get('max_price'))
		obj_set = obj_set.filter(price__lte=tmp)
		filt['max_price'] = tmp
		
	if request.POST.get('brand_name'):
		tmp = request.POST.get('brand_name')
		obj_set = obj_set.filter(brand__name=tmp)
		filt['brand_name'] = tmp
		
	if request.POST.get('is_smart'):
		tmp = bool(request.POST.get('is_smart'))
		obj_set = obj_set.filter(is_smart=tmp)
		filt['is_checked'] = True
		
	if request.POST.get('min_brightness'):
		tmp = int(request.POST.get('min_brightness'))
		obj_set = obj_set.filter(brightness__gte=tmp)
		filt['min_brightness'] = tmp
		
	if request.POST.get('min_hdmi'):
		tmp = int(request.POST.get('min_hdmi'))
		obj_set = obj_set.filter(hdmi_num__gte=tmp)
		filt['min_hdmi'] = tmp
		
	if request.POST.get('min_vga'):
		tmp = int(request.POST.get('min_vga'))
		obj_set = obj_set.filter(vga_num__gte=tmp)
		filt['min_vga'] = tmp
		
	
	return (obj_set, filt)
	
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
	
	we = WatchEntry()
	we.item = obj.unique_id
	we.date = date=datetime.now()
	we.region = get_client_ip(request)
	we.save()
	
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
	
def get_filter(context, cat_name):
	template = loader.get_template('shopapp/filters/' + cat_name + '_filter.html')
	return template.render(context)
	
	
