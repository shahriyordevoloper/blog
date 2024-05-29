from rest_framework import serializers
from .models import Post,Comment
from django.contrib.auth.models import User

class ChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','post', 'date','text')

class ParentSerializer(serializers.ModelSerializer):
    children = ChildSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title','text','img','category','date','tags','views','children')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    
class AddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title','text','img','category','date','tags')

    
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Add any additional fields if needed

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return 

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
