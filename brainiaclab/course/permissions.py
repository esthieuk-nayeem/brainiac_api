from rest_framework.permissions import BasePermission

class IsAdminUserPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            # Check if the user belongs to the admin group
            return request.user.groups.filter(name='admin').exists()
        return False
    



class IsTeacherUserPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            # Check if the user belongs to the admin group
            return request.user.groups.filter(name='teacher').exists()
        return False
    



class IsStudentUserPermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated
        if request.user and request.user.is_authenticated:
            # Check if the user belongs to the admin group
            return request.user.groups.filter(name='student').exists()
        return False
