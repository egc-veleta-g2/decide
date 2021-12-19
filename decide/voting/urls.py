from django.urls import path
from . import views


urlpatterns = [
    path('', views.VotingView.as_view(), name='voting'),
    path('<int:voting_id>/', views.VotingUpdate.as_view(), name='voting'),
    path('type/', views.chooseTypeQuestion, name='voting'),
    path('dichotomy/', views.dichotomyQuestion, name='voting'),
]
