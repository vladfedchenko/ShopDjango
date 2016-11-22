from django.db import models

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
	unique_id = models.ForeignKey(UniqueID, on_delete=models.CASCADE)
	price = models.FloatField()
	
	def __str__(self):
		return str(self.id) + ". " + str(self.brand) + ', ' + str(self.model)
	
	class Meta:
		abstract = True
	
	
class TV(ShopItem):
	diagonal = models.FloatField()
	is_smart = models.BooleanField()
	
	
