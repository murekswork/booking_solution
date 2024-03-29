from rest_framework import permissions


class IsNotAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        return not super().has_permission(request, view)
