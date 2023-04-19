from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.TextField()
    
class Hackathon(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    bg_img = models.ImageField(upload_to='bg_images/', null=True)
    hackathon_img = models.ImageField(upload_to='images/', null=True)
    submission = models.CharField(max_length=200, null=True)
    start_datetime = models.TextField(null=True)
    end_datetime = models.TextField(null=True)
    reward_prize = models.IntegerField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, default=False)
    