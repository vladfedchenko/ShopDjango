from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import *

categories = {'tv' : ('TVs', TV),
				'monitor' : ('Monitors', Monitor),
				'projector' : ('Projectors', Projector)}
				
rows = 4
cols = 4

def index(request):
	context = {'categories' : categories}
	return render(request, 'shopapp/categories.html', context)
	
def category(request, category_val, page):
	count = rows * cols
	page = int(page)
	start = (page - 1) * count
	finish = page * count
	cls = categories[category_val][1]
	
	obj_list = cls.objects.filter()[start:finish].all()
	
	context = {'objects' : obj_list,
				'rows' : range(rows),
				'cols' : range(cols)}
	
	#tv = cls.objects.get(id=1)
	return render(request, 'shopapp/category.html', context)
	
def create_item_cell(obj):
	template = loader.get_template('shopapp/item_cell.html')
	context = {'object' : obj}
	return template.render(context)
	
	
