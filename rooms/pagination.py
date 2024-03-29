from rest_framework.pagination import LimitOffsetPagination


class RoomsPagination(LimitOffsetPagination):

    default_limit = 2000
    max_limit = 1000
