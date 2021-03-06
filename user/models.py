from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone 
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.models import CloudinaryField
from django.template.defaultfilters import slugify
import datetime
import os

User._meta.get_field('email')._unique = True
User._meta.get_field('username')._unique = True

cloudinary.config( 
  secure=True,
  cloud_name = 'CLOUDINARY_CLOUD_NAME', 
  api_key = 'CLOUDINARY_API_KEY', 
  api_secret = 'CLOUDINARY_API_SECRET' 
)

class UserDetail(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=50, blank=True)
    portfolio_site = models.URLField(blank=True)
    profile_picture = CloudinaryField('image', null=True, blank=True, default="logo.png")
    def __str__(self):
        return self.user.username

class Post(models.Model): 

    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    slug = models.SlugField(max_length=50)
    title = models.CharField(max_length=50) 
    post_image = CloudinaryField('image', blank=True, null=True, default="logo.png")
    content = models.TextField() 
    published_date = models.DateTimeField(default=timezone.now) 

    def publish(self): 
        self.published_date = timezone.now() 
        self.save() 

    def __str__(self): 
        return self.title 

    def save(self):
        super(Post, self).save()
        cur_time = datetime.datetime.now()
        self.slug = '%s-%d%d%d%d%d%d' % (
            slugify(self.title), cur_time.hour, cur_time.minute, cur_time.second, cur_time.day, cur_time.month, cur_time.year
        )
        super(Post, self).save()
