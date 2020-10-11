from .models import AuctionList, WatchList, Category

def add_variable_to_context(request):
    return {
        "countCategories": Category.objects.all().count(),
        'countWatchList': WatchList.objects.filter(created_by_id=request.user.id).count()
    }