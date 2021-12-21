from django.urls import path
from .views import BoothView, BoothUrlView


id ='<int:voting_id>/'
url='<voting_url>'



urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('<voting_url>/', BoothUrlView.as_view())
]
