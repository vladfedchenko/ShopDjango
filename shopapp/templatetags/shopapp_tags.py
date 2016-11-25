from django import template
from ..views import create_item_cell

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
