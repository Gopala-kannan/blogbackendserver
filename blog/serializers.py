from rest_framework import serializers
from .models import BlogPost
from django.contrib.auth.models import User

class BlogPostRegister(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    
    class Meta:
        model = User 
        fields = [
            'username',
            'password',
            'email',
            'confirm_password',
        ]
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("passwords do not match")
        return data 
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost 
        fields = '__all__'
        extra_kwargs = {
            'author': {'read_only': True},
            'show_image': {'required': False},
        }