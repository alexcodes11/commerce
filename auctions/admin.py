from django.contrib import admin
from .models import User, CreateListing, Watchlist
# Register your models here.
admin.site.register(User)
admin.site.register(CreateListing)
admin.site.register(Watchlist)
