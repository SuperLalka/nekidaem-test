from rest_framework import permissions


class MasterPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and
                    request.user.extendinguser.blog.first().id == request.data['blog'])
