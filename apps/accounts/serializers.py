"""
 serializer file
"""
from rest_framework import serializers

from apps.accounts.choice import UserType
from apps.accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    used to serialize user objects
    """

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        """ used to create user object"""
        user = User.objects.create(email=validated_data['email'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'],
                                   is_active=True
                                   )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    """
    used to login user
    """

    email = serializers.CharField(required=True, max_length=20)
    password = serializers.CharField(required=True, max_length=20)

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        """ validate user object and user credential"""
        user = User.objects.filter(email__iexact=attrs['email']).first()

        if not user:
            raise serializers.ValidationError({'msg': 'User does not exist'})
        if not user.check_password(raw_password=attrs['password']):
            raise serializers.ValidationError({'msg': 'Password is not correct'})
        attrs['user'] = user
        return attrs


class UserListSerializer(serializers.ModelSerializer):
    """ used to serialize user object list"""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class SuperAdminSerializer(serializers.ModelSerializer):
    """
    used to serializer user objects
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'user_type', 'password')

    def create(self, validated_data):
        """ used to create user object """
        user = User.objects.create(email=validated_data['email'],
                                   first_name=validated_data['first_name'],
                                   last_name=validated_data['last_name'],
                                   user_type=validated_data['user_type'],
                                   is_active=True
                                   )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ForgotPasswordSerializer(serializers.ModelSerializer):
    """
    used to validate the student user credentials
    """
    email = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=20, required=True)

    class Meta:
        """ meta class """
        model = User
        fields = ('email', 'password')

    def validate(self, attrs):
        """ used to validate the incoming data """
        user = User.objects.filter(email__iexact=attrs['email'],
                                   user_type__in=[UserType.STUDENT.value],
                                   is_active=True,
                                   ).first()

        if not user:
            raise serializers.ValidationError({'detail': 'email-does-not-exist'})

        return attrs

    def create(self, validated_data):
        """ used to update user password"""
        user = User.objects.get(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user
