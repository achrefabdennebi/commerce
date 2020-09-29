from .models import AuctionList

def add_variable_to_context(request):
    return {
        'countWatchList': AuctionList.objects.filter(watchlist=True).count()
    }