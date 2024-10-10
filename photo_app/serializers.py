from rest_framework import serializers
from .models import Tag, User, Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Tag
#         fields = "__all__"
# serializers.py


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["author", "caption"]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
