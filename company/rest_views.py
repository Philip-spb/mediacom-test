from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from company.models import Department, User
from company.serializers import DepartmentSerializer, UserSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return None


class UserFilter(filters.FilterSet):
    last_name = filters.CharFilter(field_name='last_name')
    department = filters.NumberFilter(field_name='current_department__pk')


class UserMVS(viewsets.ModelViewSet):
    """
     Список всех пользователей

     Для фильтрации укажите следующие параметры
     ---
        - name: last_name
          description: Фамилия сотрудника
          required: False
          type: string
        - name: department
          description: ID отдела
          required: False
          type: integer
    """
    filterset_class = UserFilter
    permission_classes = (IsAuthenticated,)
    http_method_names = ['delete', 'post', 'get']
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return self.filterset_class(self.request.GET, queryset=queryset).qs


class DepartmentMVS(viewsets.ModelViewSet):
    """
    Список всех департаментов

    фильтрация недоступна
    """
    permission_classes = (AllowAny,)
    http_method_names = ['get']
    pagination_class = None
    authentication_classes = (CsrfExemptSessionAuthentication,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
