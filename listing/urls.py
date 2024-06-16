from django.urls import path
from .views import ManageListingView, ListingDetailView, ListingsView, SearchListingsView


urlpatterns = [
    path('manage/', ManageListingView.as_view(), name='listing-list'),
    path('detail/', ListingDetailView.as_view(), name='listing-list'),
    path('', ListingsView.as_view(), name='listing-list'),
    path('search', SearchListingsView.as_view(), name='listing-list'),
]
