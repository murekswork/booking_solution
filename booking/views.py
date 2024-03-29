from django.core.exceptions import ValidationError
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from booking.models import Booking
from booking.serializers import BookingSerializer, BookingSerializerUpdateStatusOnly
from common.mixins import UserQuerySetMixin


class BookingListCreateAPIView(UserQuerySetMixin, ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()
    allow_superuser_view = False

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary='Create booking',
        operation_description='Create a new booking',
        responses={403: 'not logged in',
                   409: 'dates are already taken'}
    )
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ValidationError:
            return JsonResponse(status=status.HTTP_409_CONFLICT, data={'detail': 'dates are already taken'})

    @swagger_auto_schema(
        operation_summary='List of users bookings',
        operation_description='List of authenticated users bookings',
        responses={403: 'not logged in'}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class BookingRetrieveUpdateAPIView(UserQuerySetMixin, RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializerUpdateStatusOnly
    lookup_field = 'pk'
    allow_superuser_view = True
    user_field = 'user'
    queryset = Booking.objects.all()
    http_method_names = ('patch', 'get',)

    @swagger_auto_schema(
        operation_summary='Change booking status',
        operation_description='Change booking status',
        responses={409: 'dates are already taken',
                   404: 'no booking matching given query found',
                   403: 'not logged in'}
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
