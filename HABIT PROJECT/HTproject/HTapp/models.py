from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class HT(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    HT_name = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.HT_name
    