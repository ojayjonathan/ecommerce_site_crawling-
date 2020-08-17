from django.db import models
from django.contrib.auth import get_user_model
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20,null=True, blank=True, db_index=False)
    last_name = models.CharField(max_length=20,null=True, blank=True, db_index=False)
    #profile_pic = models.
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    thumbnail = ImageSpecField(source='image',
                             processors=[Thumbnail(128,128)],
                             format='JPEG',
                             options={'quality':60})
    email = models.EmailField(null=True)

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=12)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=50, null=True, blank=True)


