import datetime
from django.db import models

# Create your models here.
class Product(models.Model):
  name = models.CharField(max_length=50, null=False, blank=False)
  description = models.TextField(max_length=100, blank=True)
  photo = models.ImageField(upload_to="images/%Y/%m/%d/", blank=True)
  price = models.FloatField(null=False)
  quantity = models.IntegerField(null=False)

  def __str__(self):
    return self.name
  
class Sale(models.Model):
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity_sold = models.IntegerField(null=False)
  sale_date = models.DateField(default=datetime.date.today, blank=False)

  def __str__(self):
    return self.product.name

class Company(models.Model):
  company_name = models.CharField(max_length=50, null=False, blank=False)
  total_revenue = models.FloatField(null=False)

  def __str__(self):
    return self.company_name

  