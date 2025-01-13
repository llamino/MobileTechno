# mobile/models.py
from django.db import models

class Mobile(models.Model):
    product_id = models.IntegerField(primary_key=True, unique=True, db_index=True)
    name = models.CharField(max_length=100,unique=True)
    image_url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_index=True)
    cpu = models.CharField(max_length=100, null=True, blank=True)
    memory = models.CharField(max_length=100, null=True, blank=True)
    ram = models.CharField(max_length=100, null=True, blank=True)
    monitor_size = models.CharField(max_length=100, null=True, blank=True)
    back_camera = models.CharField(max_length=100, null=True, blank=True)
    battery = models.CharField(max_length=100, null=True, blank=True)
    added_time = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.name

