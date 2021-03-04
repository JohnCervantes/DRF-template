from rest_framework import serializers
from .models import *


class HelloSerializer(serializers.Serializer):
    """ Serializes a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializes a user profile model obkect """
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'name', 'password', 'attribute_one',
                  'attribute_two', 'attribute_three')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        """ Create and return a new user """
        user = UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            attr1=validated_data['attribute_one'],
            attr2=validated_data['attribute_two'],
            attr3=validated_data['attribute_three'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)
