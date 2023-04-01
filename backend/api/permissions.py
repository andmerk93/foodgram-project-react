from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS


class FoodgramCurrentUserOrAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if type(obj) == type(user) and obj == user:
            return True
        return request.method in SAFE_METHODS or user.is_staff
