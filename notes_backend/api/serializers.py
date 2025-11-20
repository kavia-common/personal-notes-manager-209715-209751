from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note

# PUBLIC_INTERFACE
class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer to register a new user with username and password."""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user


# PUBLIC_INTERFACE
class NoteSerializer(serializers.ModelSerializer):
    """Serializer for Note model. Owner is read-only and set from request user."""
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Note
        fields = ("id", "title", "content", "owner", "created_at", "updated_at")
        read_only_fields = ("id", "owner", "created_at", "updated_at")
