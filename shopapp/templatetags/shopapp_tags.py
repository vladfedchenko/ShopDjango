from django import template

register = template.Library()

@register.simple_tag
def get_cell_content(*args, **kwargs):
	l = args[0]
	r = int(args[1])
	c = int(args[2])
	
	cols = int(args[3])
	
	cell = r * cols + c
	
	if len(l) <= cell:
		return ""
	else:
		return l[cell].model
