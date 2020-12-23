from django.shortcuts import render

from django.http import JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from modelUser.views import UserController

from modelUser.models import User
from modelUser.serializers import UserSerializer

userController = UserController()


@csrf_exempt
def request_test(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        print(data)

        users = userController.delete(5)

        print(users)

        return JsonResponse({
            'message': True,
        })
