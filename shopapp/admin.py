from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(UniqueID)
admin.site.register(ItemType)
admin.site.register(Brand)
admin.site.register(TV)
admin.site.register(Monitor)
admin.site.register(Projector)

