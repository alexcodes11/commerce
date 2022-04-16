# Auctions App
In this project I replicated the way Ebay works using Django, HTML, CSS, and Bootstrap. You can access the website through this link: https://alexs-auctions-site.herokuapp.com/

# How this project works
### I created many Django functions to make it work. Let's name a couple of them: ###
* **Logging in**
  * you are able to login with both username and email. Since nowadays applications accept either or
* **Registering**
* **Logging out**
* **Create a listing**
  * Each user can put a listing for sale. Then Django dynamically makes it for them and posts it in active listing section.
  * Within each listing other users are able to:
    * comment on the listing
    * bid on the listing
  * The user can then close the listing. Once the user closes the listing the highest bidder wins!
* **Watchlist function**
  * Here the user is able to add any active listing into their watchlist
* **Categories Function**
  * Just like most online websites today you can search for products based on the category for example, gaming. Well in this project I made sure to 
add a category section so you can query through the speficic category you want. 

#### This was the first project I messed around with data and django models. I realized all of this really helps to make your webpages more dynamic. ####
