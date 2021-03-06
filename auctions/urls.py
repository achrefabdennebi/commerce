from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_listing", views.add_listing_view , name="add_listing"),
    path("listings/<int:listing_id>", views.view_detail_listing ,name="listing_detail"),
    path("close_list/<int:listing_id>", views.close_list, name="close_list"),
    path("add/<int:listing_id>", views.add_watch_list ,name="add_watch_list"),
    path("remove/<int:listing_id>", views.remove_watch_list ,name="remove_watch_list"),
    path("place_comment/<int:listing_id>", views.place_comment, name="place_comment"),
    path("add_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("watchlist", views.view_watchlist, name="watchlist"),
    path("categories", views.view_categories, name="categories"),
    path("category/<str:category_name>", views.view_auction_list_by_category, name="view_auction_list_by_category"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
