from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Max
from .models import User, AuctionList, Category, Bid, WatchList, Comment
import datetime


class NewFormAuctionList(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(
        attrs={
            'class':'form-control'
        }
    ))
    description = forms.CharField(widget=forms.Textarea(attrs={"cols":23, "rows":5, "placeholder": "Description", "class":"form-control"}))
    price = forms.FloatField(label="Price", widget=forms.TextInput(
        attrs={
            'class':'form-control'
        }
    ))
    image_url = forms.CharField(label="Image url", widget=forms.TextInput(
        attrs={
            'class':'form-control'
        }
    ))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), 
                                  label="Category", widget=forms.Select(
        attrs={
            'class':'form-control'
        }
    ),  required=False)


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
            createdBy = request.user
            # Create auction item
            auctionItem = AuctionList.objects.create(
                            title = title, 
                            description= description, price = price, 
                            image_url= image_url, 
                            created_date = date, 
                            active = True,
                            category= category,
                            createdBy=request.user
                          )
            
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/listing.html", {
        "title": "Create listing",
        "formAuctionList": NewFormAuctionList()
    })


def view_detail_listing(request, listing_id):
    listing_detail = AuctionList.objects.get(pk=listing_id)
    count_bids = Bid.objects.filter(auctionList_id=listing_id).count()
    # check if this list is winned or not
    bid = Bid.objects.filter(auctionList_id=listing_id, isWinned=True, bidedBy_id=request.user.id).first()
    isWatched = WatchList.objects.filter(auctionList_id=listing_id, created_by_id=request.user.id).exists() 
    
    # Comments
    comments = Comment.objects.filter(auction_list=listing_id)
    print(f"comment: {comments}")
    if (bid is not None) and (listing_detail.active==False):
        messages.add_message(request, messages.SUCCESS, 'You have winned the bid, now you need to buy the list')
    
    return render(request, "auctions/listing_detail.html", {
        "title": "Listing", 
        "listing": listing_detail,
        "bids": count_bids,
        "isWatched": isWatched,
        "comments": comments
    })

@login_required(login_url='/login')
def view_watchlist(request):
    watchList = WatchList.objects.filter(created_by_id=request.user.id)
    auctions = []
    for watchListItem in watchList:
        auctions.append(watchListItem.auctionList)

    return render(request,  "auctions/index.html", {
        "title": "Watchlist",
        "auctions": auctions
    }) 


def view_categories(request):
    categories = Category.objects.all()
    categories_counted = []
    for category in categories:
        current_counted_item = {
            "name": category.name,
            "counted": AuctionList.objects.filter(active=True, category__name=category.name).count()
        }
        categories_counted.append(current_counted_item)

    print(categories_counted)
    return render(request, "auctions/categories.html", {
        "title": "List Categories",
        "categories": categories_counted
    })

def view_auction_list_by_category(request, category_name): 
    return render(request, "auctions/index.html", {
        "title": f"List of {category_name.lower()} active list",
        "auctions": AuctionList.objects.filter(active=True, category__name=category_name)
    }) 

def place_bid(request, listing_id):
    if request.method == "POST":
        bid_value = request.POST["bid_value"]
        print(bid_value)
        auctionList = AuctionList.objects.get(pk=listing_id)
        max_bid = Bid.objects.filter(auctionList_id=listing_id).aggregate(Max('value'))
        if (max_bid['value__max'] is None) or (float(max_bid['value__max']) < float(bid_value)):
            # Mode create a new bid
            date = datetime.datetime.now()
            Bid.objects.create(value=bid_value, 
                            auctionList=auctionList, 
                            created_date=date,
                            bidedBy=request.user
                            )
            messages.add_message(request, messages.SUCCESS, 'Your bid is the greatest, good luck')
        else:
            messages.add_message(request, messages.ERROR, 'Your bid is lower than current bid, you must add a greater bid')
            HttpResponseRedirect(reverse("listing_detail", args=(listing_id,)))
        
    return HttpResponseRedirect(reverse("listing_detail", args=(listing_id,)))


def close_list(request, listing_id):
    if request.method == "POST":
        # Select auction list
        auction = AuctionList.objects.get(pk=listing_id);
        auction.active = False
        # Select Max bid
        max_bid = Bid.objects.filter(auctionList_id=listing_id).aggregate(Max('value'))['value__max']
        if max_bid is not None: 
            bid = Bid.objects.filter(auctionList_id=listing_id, value=max_bid).first()
            bid.isWinned = True
            # Save models
            bid.save()
        auction.save()
    return HttpResponseRedirect(reverse("index"))

def add_watch_list(request, listing_id):
    if request.method == "POST":
        listing = AuctionList.objects.get(pk=listing_id)
        WatchList.objects.create(
            auctionList = listing,
            created_by = request.user
        )

        return HttpResponseRedirect(reverse("watchlist"))

def place_comment(request, listing_id):
    if request.method == "POST":
        comment_value = request.POST["content_comment"]
        date = datetime.datetime.now()
        listing = AuctionList.objects.get(pk=listing_id)
        Comment.objects.create(
            content= comment_value,
            created_date= date,
            auction_list= listing,
            created_by= request.user
        )

    return HttpResponseRedirect(reverse("listing_detail", args=(listing_id,)))

def remove_watch_list(request, listing_id):
    if request.method == "POST":
        WatchList.objects.filter(auctionList_id=listing_id, created_by_id=request.user.id).delete() 

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
