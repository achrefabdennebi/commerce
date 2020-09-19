from django.contrib import admin

from .models import AuctionList, Comment, Bid
# Register your models here.

admin.site.register(AuctionList)
admin.site.register(Bid)
admin.site.register(Comment)
