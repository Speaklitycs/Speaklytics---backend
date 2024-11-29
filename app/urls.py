from django.urls import path
from app.backend.views import ErrorDetailView, VideoUploadView

urlpatterns = [
    path('error/<str:name>/', ErrorDetailView.as_view(), name='error-detail'),
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
]
