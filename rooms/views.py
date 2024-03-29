import django_filters
from rest_framework.generics import ListAPIView

from rooms.models import Room
from rooms.serializers import RoomSerializer

from .filters import RoomFilter
from .pagination import RoomsPagination


class RoomListAPIView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = RoomFilter
    pagination_class = RoomsPagination
