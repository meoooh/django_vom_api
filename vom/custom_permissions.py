from rest_framework import permissions

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        elif obj.owner == request.user:
            return True

        # Instance must have an attribute named `owner`.
        return request.user.is_staff == True