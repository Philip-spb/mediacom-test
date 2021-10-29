from rest_framework import serializers

from company.models import Department, User


class DepartmentSerializer(serializers.ModelSerializer):
    director_id = serializers.IntegerField(required=False, label='ID директора')

    class Meta:
        model = Department
        fields = ('id', 'name', 'director_id', 'total_workers', 'salary_fund')

    def validate_director_id(self, value):
        user = User.objects.filter(pk=value)

        if not user:
            raise serializers.ValidationError(f'Пользователя с id {value} не существует')

        user = user.first()

        if user.current_department is not None and user.current_department != self.instance.pk:
            raise serializers.ValidationError(f'Пользователя с id {value} находится в другом департаменте')

        return value


class UserSerializer(serializers.ModelSerializer):
    current_department_id = serializers.IntegerField(required=False, label='ID департамента')
    current_department = serializers.SerializerMethodField(read_only=True, required=False, label='ID департамента')
    total_projects = serializers.SerializerMethodField(read_only=True, required=False, label='Количество проектов')

    class Meta:
        model = User
        fields = ('id', 'username', 'current_department_id', 'current_department', 'position', 'first_name',
                  'last_name', 'patronymic', 'age', 'photo', 'total_projects')

    def get_current_department(self, obj):
        response = None
        if obj.current_department:
            response = obj.current_department.name
        return response

    def get_total_projects(self, obj):
        projects = obj.all_employees.count()

        return projects
