from django.urls import include, path
from rest_framework import routers
from .views import dummy_view

app_name = 'testing'
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('dummy/', dummy_view, name="dummy"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]