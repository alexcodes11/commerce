from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
from django import forms


from .models import Comment, User, CreateListing, Watchlist, Bid, Category


def index(request):
    query_results = CreateListing.objects.filter(active = True)
    return render(request, "auctions/index.html",{
        "query_results": query_results,
        'categories': Category.objects.all()
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        userinput = request.POST["userinput"]
        if User.objects.filter(email=userinput).exists():
            username = User.objects.get(email=userinput).username
        elif User.DoesNotExist:
            username = request.POST['userinput']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username/email and/or password."
                })

    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            if User.objects.filter(email=email).exists():
                return render(request, "auctions/register.html", {
                    "message": "Email is already taken."
                    })
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        category = request.POST["category"]
        item = Category.objects.get(name = category)
        image = request.POST["image"]
        listing = CreateListing.objects.create(seller=request.user, title= title, description= description, image = image, setprice= bid, category = item, date_created= datetime.datetime.now(), active = True)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        choices = Category.objects.all()
        mylist = []
        for item in choices:
            mylist.append(item)
        return render(request, "auctions/create.html", {"mylist":mylist, 'categories': Category.objects.all()})


def listing(request, listing_id):
    if request.method == "GET":
        item = CreateListing.objects.get(pk=listing_id)
        test = Watchlist.objects.filter(user = request.user, item= item).exists()
        information = Comment.objects.all()
        if CreateListing.objects.filter(pk= listing_id, active= False):
            winner = Bid.objects.filter(item_id = listing_id).latest('person')
            return render(request, "auctions/listing.html", {
                    "item": item,
                    "test": test,
                    "information": information,
                    "winner": winner
                    })
        else:
            return render(request, "auctions/listing.html", {
                "item": item,
                "test": test,
                "information": information
            })


@login_required
def watchlist_add(request, listing_id):
    if request.method == "POST":
        watch = CreateListing.objects.get(pk=listing_id)
        test = Watchlist.objects.filter(user = request.user, item= watch).exists()
        if test:
            Watchlist.objects.filter(user= request.user, item = watch).delete()
            return redirect("listing", listing_id)
        Watchlist.objects.create(user= request.user, item = watch)
        return redirect("listing", listing_id)

@login_required
def watchlist(request):
    if request.method == "GET":
        query_results = Watchlist.objects.filter(user = request.user)
        return render(request, "auctions/watchlist.html", {
            "query_results": query_results,
            'categories': Category.objects.all()
        })

@login_required
def bid(request, listing_id):
    if request.method == "POST":
        bid = request.POST["bid"]
        if CreateListing.objects.filter(setprice__gte = bid, pk=listing_id).exists():
            item = CreateListing.objects.get(pk=listing_id)
            test = Watchlist.objects.filter(user = request.user, item= item).exists()
            return render(request, "auctions/listing.html", {
                "item": item,
                "test": test,
                "bid": bid,
                "message": "You need to bid above the current price"
            })
        else:
            bidd = Bid.objects.create(userbid = bid, person = request.user, biddate = datetime.datetime.now(), item_id = listing_id)
            bidd.save()
            CreateListing.objects.filter(pk=listing_id).update(setprice = bid)
            return redirect('listing', listing_id)

@login_required
def comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        info = Comment.objects.create(person = request.user, comment = comment, item_id = listing_id )
        info.save()
        return redirect('listing' , listing_id)

@login_required
def close(request, listing_id):
    if request.method == "POST":
        CreateListing.objects.filter(pk= listing_id).update(active= False)
        return redirect('listing', listing_id)

@login_required
def category(request, category_id):
    if request.method == "GET":
        result = CreateListing.objects.filter(category = category_id)
        name = Category.objects.only('name').get(pk = category_id)
        return render(request, 'auctions/category.html', {'result': result, 'name':name, 'categories': Category.objects.all()})
