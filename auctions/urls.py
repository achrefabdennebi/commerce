from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_listing", views.add_listing_view , name="add_listing"),
    path("listings/<int:listing_id>", views.view_detail_listing ,name="listing_detail"),
    path("close_list/<int:listing_id>", views.close_list, name="close_list"),
    path("add/<int:listing_id>", views.toggle_watch_list ,name="add_watch_list"),
    path("add_bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("watchlist", views.view_watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
