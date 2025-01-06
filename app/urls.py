from django.urls import path, re_path
from app.backend.views import *

urlpatterns = [
    path('api/ticket/video', VideoUploadView.as_view(), name='video-upload'),
    path('api/ticket/new', NewTicketView.as_view(), name='new-ticket'),
    path('api/ticket/stream', VideoStreamView.as_view(), name='ticket-stream'),
    path('api/ticket/analyze', TicketAnalyzeView.as_view(), name='ticket-analyze'),
    path('api/ticket/status', ErrorStatusView.as_view(), name='ticket-status'),
    re_path(r'^(?P<path>.+)$', proxy_to_frontend),
]
