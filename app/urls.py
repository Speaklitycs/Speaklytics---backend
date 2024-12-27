from django.urls import path
from app.backend.views import *

urlpatterns = [
    path('error/<str:name>/', ErrorDetailView.as_view(), name='error-detail'),
    path('ticket/video', VideoUploadView.as_view(), name='video-upload'),
    path('ticket/new', NewTicketView.as_view(), name='new-ticket'),
    path('ticket/stream', VideoStreamView.as_view(), name='ticket-stream'),
]
