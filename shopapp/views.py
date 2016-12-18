from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import *
from datetime import datetime
from django.urls import reverse
from pymongo import MongoClient
import sys
import redis
import ast

categories = {'tv' : ('TVs', TV),
				'monitor' : ('Monitors', Monitor),
				'projector' : ('Projectors', Projector)}
				
rows = 4
cols = 4

def write_user_params(username, post_dict, path):
	r = redis.StrictRedis(host='localhost', port=6379)
	#r.set('vlad', 'Test')
	r.set(username + ':path', path)
	r.set(username + ':post_dict', str(post_dict))
	r.bgsave()
	del r
	
def resolve_post_dictionary(request):
	if (request.method == 'POST'):
		return request.POST.dict()
	else:
		result = {}
		if (request.user.is_authenticated()):
			r = redis.StrictRedis(host='localhost', port=6379)
			
			need_to_restore = r.get(request.user.get_username() + ':need_to_restore')
			if (None != need_to_restore):
				r.delete(request.user.get_username() + ':need_to_restore')
				dict_str = r.get(request.user.get_username() + ':post_dict')
			
				if (None != dict_str):
					result = ast.literal_eval(dict_str.decode('ascii'))	
			
			del r
		return result
			

def index_force(request):
	if (request.user.is_authenticated()):
		r = redis.StrictRedis(host='localhost', port=6379)
		r.delete(request.user.get_username() + ':path')
		r.delete(request.user.get_username() + ':post_dict')
		del r
	return HttpResponseRedirect(reverse('shopapp:index'))

def index(request):
	if (request.user.is_authenticated()):
		
		r = redis.StrictRedis(host='localhost', port=6379)
		path = r.get(request.user.get_username() + ':path')
		if (None != path):
			r.set(request.user.get_username() + ':need_to_restore', '1')
		del r
		if (None != path):
			return HttpResponseRedirect(path)
		
	return render(request, 'shopapp/index.html')
	
def category(request, category_val, page):
	
	post_dict = resolve_post_dictionary(request)
	
	if (request.user.is_authenticated()):
		write_user_params(request.user.get_username(), post_dict, request.path)
	
	count = rows * cols
	
	if post_dict.get('action_button'):
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
	
	obj_list, filt = filter_objects(post_dict, cls.objects)
	
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
	
def filter_objects(post_dict, obj_set):
	
	filt = {}
	if post_dict.get('min_price'):
		tmp = float(post_dict.get('min_price'))
		obj_set = obj_set.filter(price__gte=tmp)
		filt['min_price'] = tmp
	
	if post_dict.get('max_price'):
		tmp = float(post_dict.get('max_price'))
		obj_set = obj_set.filter(price__lte=tmp)
		filt['max_price'] = tmp
		
	if post_dict.get('brand_name'):
		tmp = post_dict.get('brand_name')
		obj_set = obj_set.filter(brand__name=tmp)
		filt['brand_name'] = tmp
		
	if post_dict.get('is_smart'):
		tmp = bool(post_dict.get('is_smart'))
		obj_set = obj_set.filter(is_smart=tmp)
		filt['is_checked'] = True
		
	if post_dict.get('min_brightness'):
		tmp = int(rpost_dict.get('min_brightness'))
		obj_set = obj_set.filter(brightness__gte=tmp)
		filt['min_brightness'] = tmp
		
	if post_dict.get('min_hdmi'):
		tmp = int(post_dict.get('min_hdmi'))
		obj_set = obj_set.filter(hdmi_num__gte=tmp)
		filt['min_hdmi'] = tmp
		
	if post_dict.get('min_vga'):
		tmp = int(post_dict.get('min_vga'))
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
	
	context = {}
	
	cls = categories[category_val][1]
	obj = get_object_or_404(cls, pk=obj_id)
	
	context['obj'] = obj
	
	client = MongoClient()
	
	comment_item = client['shop'].comments.find_one({u'object_uid' : str(obj.unique_id.id)})
	#return HttpResponse(str(comment_item))
	
	if (not (comment_item is None)):
		
		context['aver_mark'] = comment_item[u'aver_mark']
		context['comments'] = comment_item[u'comments_marks']
		
		comment_entry_l = [x for x in comment_item[u'comments_marks'] if x[u'user_id'] == request.user.id]
		
		if (len(comment_entry_l) != 0):
			entry = comment_entry_l[0]
			context['mark' + str(entry[u'mark'])] = True
			context['comment'] = entry[u'comment']
			
			#return HttpResponse(str(context))
			
		else:
			context['mark5'] = True
			context['comment'] = ''
			#return HttpResponse(str(context))
			
	else:
		context['mark5'] = True
		context['comment'] = ''
		#return HttpResponse(str(context))
	
	del client
		
	#return HttpResponse(str(context))	
	
	we = WatchEntry()
	we.item = obj.unique_id
	we.date = date=datetime.now()
	we.region = get_client_ip(request)
	we.save()
	
	
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

def get_new_comment(obj_uid):
	comment = {}
	comment[u'object_uid'] = obj_uid
	comment[u'aver_mark'] = 0.0
	comment[u'comment_count'] = 0
	comment[u'comments_marks'] = []
	
	return comment
	

def leave_comment(request, obj_uid):
	client = MongoClient()
	comment_item_tmp = client['shop'].comments.find_one_and_delete({u'object_uid' : obj_uid})
	
	#return HttpResponse(str(comment_item_tmp))
	
	if (comment_item_tmp is None):
		comment_item = get_new_comment(obj_uid)
	else:
		comment_item = comment_item_tmp
		
	comment_entry_l = [x for x in comment_item[u'comments_marks'] if x[u'user_id'] == request.user.id]
	if (len(comment_entry_l) == 0):
		entry = {}
		entry[u'user_id'] = request.user.id
		entry[u'username'] = request.user.username
		entry[u'comment'] = request.POST['comment']
		mark = int(request.POST['mark'])
		entry[u'mark'] = mark
		
		count = comment_item[u'comment_count']
		mark_sum = comment_item[u'aver_mark'] * count
		
		new_mark = (mark_sum + mark) / (count + 1)
		comment_item[u'comment_count'] = count + 1
		comment_item[u'aver_mark'] = new_mark
		comment_item[u'comments_marks'].append(entry)
		
	else:
		entry = comment_entry_l[0]
		entry[u'comment'] = request.POST['comment']
		prev_mark = entry[u'mark']
		
		mark = int(request.POST['mark'])
		entry[u'mark'] = mark
		
		count = comment_item[u'comment_count']
		mark_sum = comment_item[u'aver_mark'] * count
		
		new_mark = (mark_sum - prev_mark + mark) / count
		comment_item[u'aver_mark'] = new_mark
		
	client['shop'].comments.insert_one(comment_item)
	
	del client
	
	return HttpResponseRedirect(reverse('shopapp:index'))
