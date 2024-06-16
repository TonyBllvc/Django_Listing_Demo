from django.urls import path
from .views import RegisterView, RetrieveUserView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-list'),
    path('user_profile/', RetrieveUserView.as_view(), name='user-list')
]
