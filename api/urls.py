from django.urls import include, path
from rest_framework import routers

from .views import create_drugstores, DrugstoreViewSet


app_name = 'api'

router = routers.DefaultRouter()

router.register('drugstores', DrugstoreViewSet, basename='drugstores')


urlpatterns = [
    path('', include(router.urls)),
    path('create_drugstores/', create_drugstores, name='create_drugstores')
]
