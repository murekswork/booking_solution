from django.core.exceptions import ValidationError
from django.http import JsonResponse
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

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ValidationError:
            return JsonResponse(status=status.HTTP_409_CONFLICT, data={'detail': 'dates are already taken'})


class BookingRetrieveUpdateAPIView(UserQuerySetMixin, RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializerUpdateStatusOnly
    lookup_field = 'pk'
    allow_superuser_view = True
    user_field = 'user'
    queryset = Booking.objects.all()

    def put(self, request, *args, **kwargs):
        return JsonResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED, data={'detail': 'method not allowed'})
