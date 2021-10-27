from django.urls import path
from rest_framework.routers import DefaultRouter

from company.rest_views import DepartmentMVS, UserMVS

app_name = 'api'

router = DefaultRouter()

router.register(r'users', UserMVS, basename='users')
router.register(r'departments', DepartmentMVS, basename='departments')

urlpatterns = router.urls