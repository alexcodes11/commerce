from django.contrib import admin
from .models import Comment, User, CreateListing, Watchlist, Bid, Category
# Register your models here.
admin.site.register(User)
admin.site.register(CreateListing)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
