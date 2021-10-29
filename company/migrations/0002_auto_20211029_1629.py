# Generated by Django 3.2.8 on 2021-10-29 13:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название проекта')),
            ],
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'ordering': ['pk'], 'verbose_name': 'Департамент', 'verbose_name_plural': 'Департаменты'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['pk'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterField(
            model_name='department',
            name='director',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, unique=True, verbose_name='Директор'),
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['last_name'], name='company_use_last_na_95f4d3_idx'),
        ),
        migrations.AddField(
            model_name='companyproject',
            name='admin',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_admin', to=settings.AUTH_USER_MODEL, verbose_name='Руководитель'),
        ),
        migrations.AddField(
            model_name='companyproject',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.department', verbose_name='Департамент'),
        ),
        migrations.AddField(
            model_name='companyproject',
            name='employees',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Департамент'),
        ),
    ]