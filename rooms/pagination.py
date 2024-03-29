from rest_framework.pagination import LimitOffsetPagination


class RoomsPagination(LimitOffsetPagination):

    default_limit = 20
    max_limit = 100
