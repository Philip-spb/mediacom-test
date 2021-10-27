from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Q

from company.models import User, Department


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'email',
        'current_department',
        'position',
        'first_name',
        'last_name',
        'salary',
        'age'
    )

    fieldsets = (
        (None, {'fields': (
            ('first_name', 'last_name'),
            ('patronymic',),
            ('birth_day',),
            ('position', 'salary',),
            ('current_department',),
            ('photo',),
        )}),
    )

    save_on_top = True

    list_select_related = (
        'current_department',
    )


@admin.register(Department)
class CompanyAdmin(admin.ModelAdmin):

    def render_change_form(self, request, context, *args, **kwargs):
        users = User.objects.filter(Q(current_department__isnull=True) | Q(current_department=kwargs['obj'].pk))
        context['adminform'].form.fields['director'].queryset = users
        return super(CompanyAdmin, self).render_change_form(request, context, *args, **kwargs)

    list_display = ('pk', 'name', 'director',)
    list_display_links = ('pk', 'name',)
    search_fields = ('name',)

    save_on_top = True
