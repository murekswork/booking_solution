from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        read_only_fields = ('active',)
        fields = ('room', 'checkin', 'checkout', 'active',)


class BookingSerializerUpdateStatusOnly(serializers.ModelSerializer):
    class Meta:
        model = Booking
        read_only_fields = ('room', 'checkin', 'checkout',)
        fields = ('room', 'checkin', 'checkout', 'active')
