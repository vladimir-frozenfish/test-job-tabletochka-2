from rest_framework import viewsets

from drugstores.models import Drugstore

from .serializers import DrugstoreSerializer, DrugstoreCreateSerializer


class DrugstoreViewSet(viewsets.ModelViewSet):
    queryset = Drugstore.objects.all()
    serializer_class = DrugstoreSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return DrugstoreSerializer
        return DrugstoreCreateSerializer