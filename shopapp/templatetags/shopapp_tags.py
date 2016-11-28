from django import template
from ..views import *

register = template.Library()

@register.simple_tag
def get_cell_content(*args, **kwargs):
	l = args[0]
	r = int(args[1])
	c = int(args[2])
	cat_name = args[4]
	
	cols = int(args[3])
	
	cell = r * cols + c
	
	if len(l) <= cell:
		return ""
	else:
		return create_item_cell(l[cell], cat_name)
		#return cat_name

@register.simple_tag		
def create_category_list():
	return categories_list()
	
@register.simple_tag(takes_context=True)
def get_filter_form(context, cat_name):
	return get_filter(context, cat_name)
