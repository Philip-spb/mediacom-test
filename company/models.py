from typing import Optional
from django.conf import settings
from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum


class User(AbstractUser):
    patronymic = models.CharField(max_length=40, verbose_name='Отчество', blank=True, null=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Фото')
    position = models.CharField(max_length=160, verbose_name='Должность', blank=True, null=True)
    salary = models.IntegerField(verbose_name='Оклад', blank=True, null=True)
    birth_day = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    current_department = models.ForeignKey('Department', on_delete=models.SET_NULL, blank=True, null=True,
                                           verbose_name='Департамент')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['pk']
        indexes = [
            models.Index(fields=('last_name',)),
        ]

    @property
    def age(self) -> Optional[int]:
        """
        Количество полных лет сотрудника
        """
        if not self.birth_day:
            return None

        today = date.today()
        birth_day = date.fromisoformat(str(self.birth_day))
        age = today.year - birth_day.year
        if today.month < birth_day.month or (today.month == birth_day.month and today.day < birth_day.day):
            age -= 1
        return age


class Department(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название', unique=True)
    director = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                 verbose_name='Директор', unique=True)

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'
        ordering = ['pk']

    def __str__(self):
        return self.name

    @property
    def total_workers(self) -> int:
        """
        Число сотрудников
        """
        return User.objects.filter(current_department=self).count()

    @property
    def salary_fund(self) -> int:
        """
        Суммарный оклад всех сотрудников департамента
        """
        return User.objects.filter(current_department=self).aggregate(sum=Sum('salary')).get('sum', None)


class CompanyProject(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название проекта', unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, verbose_name='Департамент',
                                   blank=True, null=True)
    admin = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                 verbose_name='Руководитель', related_name='project_admin')
    employees = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='Участники', related_name='all_employees')


