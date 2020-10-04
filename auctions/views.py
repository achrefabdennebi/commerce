from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User, AuctionList, Category, Bid
import datetime


class NewFormAuctionList(forms.Form):
    title = forms.CharField(label="Title")
    description = forms.CharField(widget=forms.Textarea(attrs={"cols":23, "rows":5, "placeholder": "Description"}))
    price = forms.FloatField(label="Price")
    image_url = forms.CharField(label="Image url")
    category = forms.ModelChoiceField(queryset=Category.objects.all(), 
                                  label="Category")


def index(request):
    return render(request, "auctions/index.html", {
        "title": "Active Listings",
        "auctions": AuctionList.objects.filter(active=True)
    })


def add_listing_view(request): 
    if request.method == "POST":
        form = NewFormAuctionList(request.POST)
        if form.is_valid():
            # Get data from form
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image_url = form.cleaned_data["image_url"]
            date = datetime.datetime.now()
            category = form.cleaned_data["category"]
            # Create auction item
            auctionItem = AuctionList.objects.create(
                            title = title, 
                            description= description, price = price, 
                            image_url= image_url, 
                            created_date = date, 
                            active = True,
                            category= category
                          )
            
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/listing.html", {
        "title": "Create listing",
        "formAuctionList": NewFormAuctionList()
    })


def view_detail_listing(request, listing_id):
    listing_detail = AuctionList.objects.get(pk=listing_id)
    count_bids = Bid.objects.filter(auctionList_id=listing_id).count()
    return render(request, "auctions/listing_detail.html", {
        "title": "Listing", 
        "listing": listing_detail,
        "bids": count_bids
    })


def view_watchlist(request):
    return render(request,  "auctions/index.html", {
        "title": "Watchlist",
        "auctions": AuctionList.objects.filter(watchlist=True)
    }) 

def place_bid(request, listing_id):
    if request.method == "POST":
        bid_value = request.POST["bid_value"]
        auctionList = AuctionList.objects.get(pk=listing_id)
        bid = Bid.objects.get(auctionList_id=listing_id)
        date = datetime.datetime.now()
        Bid.objects.create(value=bid_value, 
                           auctionList=auctionList, 
                           created_date=date
                           )
        print(f"Bid = {bid_value} {bid.value}")
    return HttpResponseRedirect(reverse("listing_detail", args=(listing_id,)))
 
def toggle_watch_list(request, listing_id):
    if request.method == "POST":
        listing = AuctionList.objects.get(pk=listing_id)
        listing.watchlist = not listing.watchlist
        listing.save()
        return HttpResponseRedirect(reverse("watchlist"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
