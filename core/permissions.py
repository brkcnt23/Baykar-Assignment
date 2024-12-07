from rest_framework.permissions import BasePermission

class IsTeamMember(BasePermission):
    """
    Kullanıcının kendi takımına ait nesneleri yönetmesine izin verir.
    Parça vb. üzerinde işlem yapılırken obj.team == request.user.employee.team kontrolü yapar.
    """
    def has_object_permission(self, request, view, obj):
        # Süper kullanıcıya izin verelim (opsiyonel)
        if request.user.is_staff or request.user.is_superuser:
            return True

        employee = getattr(request.user, 'employee', None)
        if employee and obj.team == employee.team:
            return True
        return False

class IsMontajTeam(BasePermission):
    """
    Sadece montaj takımının erişebilmesini sağlayan permission.
    """
    def has_permission(self, request, view):
        employee = getattr(request.user, 'employee', None)
        if employee and employee.team and employee.team.team_type == 'MONTAJ_TAKIMI':
            return True
        return False