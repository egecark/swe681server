from django.shortcuts import render
from rest_framework import viewsets

from .serializers import DummySerializer
from .models import Dummy


class DummyViewSet(viewsets.ModelViewSet):
    queryset = Dummy.objects.all().order_by('value')
    serializer_class = DummySerializer
# Create your views here.
