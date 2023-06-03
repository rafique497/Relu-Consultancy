"""
 view file
"""
# django import
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response


# local import
from apps.accounts.models import User
from apps.accounts.permissions import TeacherPermission, SuperAdminPermission
from apps.accounts.serializers import (RegisterSerializer, LoginSerializer, UserListSerializer, SuperAdminSerializer,
                                       ForgotPasswordSerializer)
from apps.accounts.utils import get_token


class LoginViewSet(GenericViewSet):
    """
    used to login user
    """

    serializer_class = LoginSerializer
    queryset = User.objects.all()

    def create(self, request):
        """used to create token for user after successfully login"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        data = {
            'user_id': user.id,
            'email': user.email,
            'user_type': user.user_type
        }
        token = get_token(data)
        return Response({'token': token})


class SuperAdminViewSet(GenericViewSet):
    """
    super admin view set
    """
    serializer_class = SuperAdminSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, SuperAdminPermission]

    def list(self, request):
        """ used to list all student and teacher"""
        queryset = self.get_queryset().filter(user_type__in=['student', 'teacher'])
        serializer = UserListSerializer(queryset, many=True)

        return Response({'data': serializer.data})

    def create(self, request):
        """ used to create student and teacher object"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TeacherViewSet(GenericViewSet):
    """
    teacher view set
    """
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, TeacherPermission]

    def list(self, request):
        """ used to access all student list"""
        queryset = self.get_queryset().filter(user_type__iexact='student')
        serializer = UserListSerializer(queryset, many=True)

        return Response({'data': serializer.data})

    def create(self, request):
        """ create student object """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class StudentViewSet(GenericViewSet):
    """
    student view set
    """
    serializer_class = UserListSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=False, url_path='profile', url_name='profile')
    def get_student(self, request, *args, **kwargs):
        """used to get student details"""
        instance = self.get_queryset().filter(user_type__iexact='student',
                                              id=request.auth.payload['user_id']).first()
        serializer = self.serializer_class(instance)

        return Response({'details': serializer.data})


class ForgotPasswordViewSet(GenericViewSet):
    """
    forgot password view set
    """
    serializer_class = ForgotPasswordSerializer
    queryset = User.objects.all()

    def create(self, request):
        """used to change password"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
