from django.db import models

class Mobile(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    added_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

