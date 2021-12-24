from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    email = models.EmailField(unique=True)
    


class CreateListing(models.Model):
    seller = models.ForeignKey(User, on_delete= models.CASCADE )
    title = models.CharField(max_length=64)
    description = models.TextField(default="None")
    setprice = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='images/')
    category = models.CharField(max_length=32, default="None")
    date_created = models.DateField()

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name="watchlist")
    item = models.ForeignKey(CreateListing, on_delete= models.CASCADE)
    

