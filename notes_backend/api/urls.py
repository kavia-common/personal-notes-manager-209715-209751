from django.urls import path
from .views import (
    health,
    RegisterView,
    ObtainAuthTokenView,
    NoteListCreateView,
    NoteDetailView,
)

urlpatterns = [
    path('health/', health, name='Health'),

    # Auth endpoints
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path('auth/token', ObtainAuthTokenView.as_view(), name='auth-token'),

    # Notes endpoints
    path('notes', NoteListCreateView.as_view(), name='notes-list-create'),
    path('notes/<int:pk>', NoteDetailView.as_view(), name='notes-detail'),
]
