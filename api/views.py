from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from drugstores.models import Drugstore

from .serializers import DrugstoreSerializer, DrugstoreCreateSerializer
from .filters import DrugstoreFilter


@api_view(['POST'])
def create_drugstores(request):
    """функция создает записи о патеках из запроса, состояещго из списка Json-запроса аптек"""
    request_len_drugstore = len(request.data)
    created_len_drugstore = 0
    for drugstore in request.data:
        serializer = DrugstoreCreateSerializer(data=drugstore)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            created_len_drugstore += 1

    return Response(
        {
            'Количество запросов на создание аптек': request_len_drugstore,
            'Создано записей о аптеках': created_len_drugstore
        },
        status=status.HTTP_201_CREATED
    )


class DrugstoreViewSet(viewsets.ModelViewSet):
    queryset = Drugstore.objects.all()
    serializer_class = DrugstoreSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = DrugstoreFilter


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DrugstoreCreateSerializer
        return DrugstoreSerializer