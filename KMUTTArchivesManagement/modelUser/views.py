from django.shortcuts import render

from modelUser.models import User
from modelUser.serializers import UserSerializer


class UserController():
    def get(self, pk):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return serializer.data

    def gets(self):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return serializer.data

    def create(self, body):
        serializer = UserSerializer(data=body)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        print(serializer.errors)
        return False

    def update(self, pk, body):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=body)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        print(serializer.errors)
        return False

    def delete(self, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return True
