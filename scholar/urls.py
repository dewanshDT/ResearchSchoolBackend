from django.urls import path
from . import views

app_name = "scholar"
urlpatterns = [
    path("search/", views.index, name="search"),
    path("login/", views.send_otp, name="send_otp"),
    path("verify_otp/<str:mobile_number>/", views.verify_otp, name="verify_otp"),
]
