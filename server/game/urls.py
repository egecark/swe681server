from django.urls import include, path
from rest_framework import routers
from .views import dummy_view

app_name = 'game'
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', dummy_view, name="main"),
    path('turn/', dummy_view, name="turn"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
