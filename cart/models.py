from django.db import models
from django.contrib.auth import get_user_model
from app.models import Bestdeal

User = get_user_model()
# Create your models here.
class UserCart(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.OneToOneField(Bestdeal, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    wishlist = models.BooleanField(default=False)
    total = models.BigIntegerField(default=1000)
    