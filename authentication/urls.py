from django.urls import path
from . import views


urlpatterns = [
    path("", views.HelloAuthView.as_view(), name="hello_auth"),
    path("signup", views.UserCreateView.as_view(), name="sign_up_view"),
    path("profile/", views.UserProfileView.as_view(), name="user_profile"),
    path("addresses/", views.AddressListView.as_view(), name="address_list"),
    path("addresses/<int:pk>/", views.AddressDetailView.as_view(), name="address_detail"),
]