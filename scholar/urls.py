from django.urls import path
from . import views

app_name = 'scholar'
urlpatterns = [
    path("search/", views.index, name="search"),
    # path("se/", views.search, name='search')
]
