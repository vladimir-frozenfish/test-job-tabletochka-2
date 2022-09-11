from django.urls import include, path
from rest_framework import routers

from .views import DrugstoreViewSet


app_name = 'api'

router = routers.DefaultRouter()

router.register('drugstores', DrugstoreViewSet, basename='drugstores')


urlpatterns = [
    path('', include(router.urls)),
]
