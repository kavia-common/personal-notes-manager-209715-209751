from rest_framework.permissions import BasePermission
from .models import Note


class IsOwner(BasePermission):
    """
    Allows access only to objects owned by the authenticated user.
    """

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Note):
            return obj.owner_id == getattr(request.user, "id", None)
        # Default deny if unknown object type
        return False
