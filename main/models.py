from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Expense(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    price=models.FloatField()
    category=models.CharField(max_length=300)
    date=models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.name