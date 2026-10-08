from rest_framework import permissions


class IsSeller(permissions.BasePermission):


    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'seller'


class IsBuyer(permissions.BasePermission):


    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'buyer'


class IsPropertyOwnerOrReadOnly(permissions.BasePermission):
   

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'seller'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.seller == request.user


class IsReviewAuthorOrReadOnly(permissions.BasePermission):


    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user