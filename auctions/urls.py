from django.urls import path


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.create_listing, name="createlisting"),
    path("listing/<int:listing_id>/", views.listing, name ="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:listing_id>/", views.watchlist_add , name="watchlist_add" ),
    path("listing/<int:listing_id>", views.bid, name="bid"),
    path("listing/comment/<int:listing_id>", views.comment, name="comment"), 
    path("listing/close/<int:listing_id>/", views.close, name="close"),
    path("category/<int:category_id>/", views.category, name = "category" )
    ]


