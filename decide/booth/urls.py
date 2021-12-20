from django.urls import path
from .views import BoothView, InicioView

urlpatterns = [
    path('<int:voting_id>/', BoothView.as_view()),
    path('inicio/', InicioView.as_view(), name="boothInicio"),
]
