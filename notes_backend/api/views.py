from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, permissions, pagination
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from .models import Note
from .serializers import UserRegistrationSerializer, NoteSerializer
from .permissions import IsOwner


@api_view(['GET'])
def health(request):
    """Simple healthcheck endpoint."""
    return Response({"message": "Server is up!"})


class DefaultPagination(pagination.PageNumberPagination):
    """Default pagination with page size 10; overridable via ?page_size."""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# PUBLIC_INTERFACE
class RegisterView(APIView):
    """Register a new user with username and password."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "username": user.username},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
class ObtainAuthTokenView(APIView):
    """Obtain an auth token using username and password."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(
                {"detail": "username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {"detail": "Invalid credentials."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})


# PUBLIC_INTERFACE
class NoteListCreateView(generics.ListCreateAPIView):
    """
    List and create notes for the authenticated user.
    Filtering: ?q=term will search in title and content (case-insensitive).
    Pagination: PageNumberPagination with ?page, ?page_size.
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        user = self.request.user
        qs = Note.objects.filter(owner=user)
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# PUBLIC_INTERFACE
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single note owned by the user.
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Limit queryset to user's notes for retrieval and lookup
        return Note.objects.filter(owner=self.request.user)
