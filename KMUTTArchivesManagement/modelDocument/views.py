from django.shortcuts import render

from modelDocumnt.models import *
from modelDocumnt.serializers import *


class DocumentController():
    def get(self, pk):
