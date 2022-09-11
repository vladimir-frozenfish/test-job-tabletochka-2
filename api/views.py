from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from drugstores.models import Drugstore

from .serializers import DrugstoreSerializer, DrugstoreCreateSerializer, NearSearilez
from .filters import DrugstoreFilter


class DrugstoreViewSet(viewsets.ModelViewSet):
    queryset = Drugstore.objects.all()
    serializer_class = DrugstoreSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = DrugstoreFilter

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return DrugstoreCreateSerializer
        return DrugstoreSerializer

    @action(['get'], detail=False)
    def near(self, request):
        """функция возвращает список аптек в указаннои радиусе
        Учитвая поиск аптек в России, то не берем сложную формулу расчета
        расстояния в заисимости от долготы.
        Исходим, что 1 км по широте равне - 0,0085
        1 км по долготе (на долготе +- 36 градусов) равен - 0,0141.

        Возвращается ближайшие аптеки не по радиусу а по стороне квадрата"""
        COEFFICIENT_LAT = 0.0085
        COEFFICIENT_LON = 0.0141

        near = NearSearilez(data=request.GET)
        near.is_valid(raise_exception=True)
        near = near.validated_data

        radius_lat = near['radius'] * COEFFICIENT_LAT
        radius_lon = near['radius'] * COEFFICIENT_LON

        drugstores = Drugstore.objects.filter(
            geo__location__lat__range=[float(near['lat']) - radius_lat, float(near['lat']) + radius_lat],
            geo__location__lon__range=[float(near['lon']) - radius_lon, float(near['lon']) + radius_lon]
        )
        page = self.paginate_queryset(drugstores)
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)


@api_view(['POST'])
def create_drugstores(request):
    """функция создает записи о аптеках из запроса, состояещго из списка Json-запроса аптек"""
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