from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)

        user = authenticate(username=username, password=password)
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
