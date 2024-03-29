from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Booking
        fields = ('room', 'checkin', 'checkout', 'active')


class BookingSerializerUpdateStatusOnly(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(read_only=True)
    checkin = serializers.DateField(read_only=True)
    checkout = serializers.DateField(read_only=True)
    active = serializers.BooleanField(read_only=False)

    class Meta:
        model = Booking
        fields = ('room', 'checkin', 'checkout', 'active')
