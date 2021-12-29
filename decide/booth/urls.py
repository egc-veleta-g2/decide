from django.urls import path
from .views import BoothView, BoothUrlView, InicioView


urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('<voting_url>/', BoothUrlView.as_view()),
    path('', InicioView.as_view(), name="boothInicio")
]
