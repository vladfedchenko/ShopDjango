from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ItemType(models.Model):
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return str(self.id) + ". " + self.name

class UniqueID(models.Model):
	item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
	
	def __str__(self):
		return str(self.id) + ". " + str(self.item_type)
	
class Brand(models.Model):
	name = models.CharField(max_length=200)
	
	def __str__(self):
		return str(self.id) + ". " + self.name
	
class ShopItem(models.Model):
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
	model = models.CharField(max_length=200)
	unique_id = models.OneToOneField(UniqueID, on_delete=models.CASCADE)
	price = models.FloatField()
	
	def __str__(self):
		return str(self.id) + ". " + str(self.brand) + ', ' + str(self.model)
	
	class Meta:
		abstract = True
	
	
class TV(ShopItem):
	diagonal = models.FloatField()
	is_smart = models.BooleanField()
	
	@classmethod
	def create(cls, brand, model, price, diagonal, is_smart):
		item_type, created = ItemType.objects.get_or_create(name='TV')
		unique_id = UniqueID(item_type=item_type)
		unique_id.save()
		tv = cls(brand=brand, model=model, unique_id=unique_id, price=price, diagonal=diagonal, is_smart=is_smart)
		tv.save()
		return tv
			
			
	
class Monitor(ShopItem):
	diagonal = models.FloatField()
	hdmi_num = models.IntegerField()
	vga_num = models.IntegerField()
	
	@classmethod
	def create(cls, brand, model, price, diagonal, hdmi_num, vga_num):
		item_type, created = ItemType.objects.get_or_create(name='Monitor')
		unique_id = UniqueID(item_type=item_type)
		unique_id.save()
		item = cls(brand=brand, model=model, unique_id=unique_id, price=price, diagonal=diagonal, hdmi_num=hdmi_num, vga_num=vga_num)
		item.save()
		return item
	
class Projector(ShopItem):
	brightness = models.IntegerField()
	hdmi_num = models.IntegerField()
	vga_num = models.IntegerField()
	
	@classmethod
	def create(cls, brand, model, price, brightness, hdmi_num, vga_num):
		item_type, created = ItemType.objects.get_or_create(name='Projector')
		unique_id = UniqueID(item_type=item_type)
		unique_id.save()
		item = cls(brand=brand, model=model, unique_id=unique_id, price=price, brightness=brightness, hdmi_num=hdmi_num, vga_num=vga_num)
		item.save()
		return item
		
class UserItem(models.Model):
	item = models.ForeignKey(UniqueID, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	price = models.FloatField()
	date = models.DateTimeField()
	region = models.GenericIPAddressField()
