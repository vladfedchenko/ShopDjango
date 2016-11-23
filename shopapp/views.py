from django.http import HttpResponse
from django.shortcuts import render
from .models import *

categories = {'tv' : ('TVs', TV),
				'monitor' : ('Monitors', Monitor),
				'projector' : ('Projectors', Projector)}

def index(request):
	context = {'categories' : categories}
	return render(request, 'shopapp/categories.html', context)
	
def category(request, category_val):
	cls = categories[category_val][1]
	#tv = cls.objects.get(id=1)
	return HttpResponse(category_val)
