from .models import AuctionList, WatchList

def add_variable_to_context(request):
    return {
        'countWatchList': WatchList.objects.filter(created_by_id=request.user.id).count()
    }