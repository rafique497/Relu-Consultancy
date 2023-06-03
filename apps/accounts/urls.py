"""
 urls file
"""
# third party imports
from rest_framework import routers

from apps.accounts.views import (LoginViewSet, TeacherViewSet, SuperAdminViewSet, StudentViewSet,
                                 ForgotPasswordViewSet)

router = routers.SimpleRouter()

router.register('login', LoginViewSet, basename='login')
router.register('teacher', TeacherViewSet, basename='teacher')
router.register('super-admin', SuperAdminViewSet, basename='super-admin')
router.register('student', StudentViewSet, basename='student')
router.register('forgot-password', ForgotPasswordViewSet, basename='forgot-password')


urlpatterns = [
]+router.urls
