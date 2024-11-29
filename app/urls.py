from django.urls import path
from app.backend.views import ErrorDetailView

urlpatterns = [
    path('error/<str:name>/', ErrorDetailView.as_view(), name='error-detail'),
]
