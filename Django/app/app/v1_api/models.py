from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=80)
    product_category = models.CharField(max_length=80, default="") 

    def __str__(self):
        return self.product_name