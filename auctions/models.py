from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
 
    def __str__(self):
        return f"{self.name}"

class AuctionList(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=250)
    price = models.FloatField()
    image_url = models.CharField(max_length=250)
    created_date = models.DateField()
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category,null=True, blank=True, on_delete=models.DO_NOTHING, related_name="categories")
    createdBy = models.ForeignKey(User,null=True, blank=True, on_delete=models.DO_NOTHING, related_name="users")

    def __str__(self):
        return f"{self.title} ({self.price})"

class WatchList(models.Model):
    auctionList = models.ForeignKey(AuctionList,null=True, blank=True, on_delete= models.CASCADE, related_name="auction_List_watch_list" )
    created_by = models.ForeignKey(User,null=True, blank=True, on_delete= models.CASCADE, related_name="users_watch_list")

    def __str__(self):
        return f'{self.auctionList} / {self.created_by}'

class Bid(models.Model):
    value = models.FloatField()
    created_date = models.DateField()
    auctionList = models.ForeignKey(AuctionList,null=True, blank=True, on_delete= models.CASCADE, related_name="auction_List" )
    bidedBy = models.ForeignKey(User,null=True, blank=True, on_delete= models.DO_NOTHING, related_name="users_bid" )
    isWinned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.auctionList.title} / {self.value} / {self.created_date}"

class Comment(models.Model):
    content = models.CharField(max_length=250, default='')
    created_date  = models.DateTimeField()
    auction_list =  models.ForeignKey(AuctionList,null=True, blank=True, on_delete= models.CASCADE, related_name="auction_List_comment")
    created_by = models.ForeignKey(User,null=True, blank=True, on_delete= models.CASCADE, related_name="users_comment")

    def __str__(self):
        return f"{self.content} / {self.created_date}"




