from django.urls import path
from .views import HomeView, CliniTENSView, FarmaTEFView

urlpatterns = [
    path("", HomeView.as_view(), name="Home"),
    path("clinitens/", CliniTENSView.as_view(), name="clinitens"),
    path("farmatef/", FarmaTEFView.as_view(), name="farmatef"),
]
