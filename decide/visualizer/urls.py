from django.urls import path
from .views import VisualizerView, VisualizerInicioView


urlpatterns = [
    path('', VisualizerInicioView.as_view(), name="visualizer_inicio"),
    path('<int:voting_id>/', VisualizerView.as_view(), name="visualizer"),
]
