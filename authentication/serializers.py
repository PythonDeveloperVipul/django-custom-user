from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',
                  'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['first_name']=='':
            raise serializers.ValidationError(
                {"first_name": "first name not be blank"})
        elif attrs['last_name']=='':
            raise serializers.ValidationError(
                {"last_name": "last name not be blank"})
        elif attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
  
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)