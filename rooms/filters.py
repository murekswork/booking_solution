from datetime import date, datetime, timedelta

import django_filters
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from booking.models import Booking
from rooms.models import Room


class RoomFilter(django_filters.FilterSet):
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    spots_gte = django_filters.NumberFilter(field_name='spots', lookup_expr='gte')
    spots_lte = django_filters.NumberFilter(field_name='spots', lookup_expr='lte')

    checkin = django_filters.DateFilter(method='get_available_rooms', field_name='available_rooms', )
    checkout = django_filters.DateFilter(method='get_available_rooms', field_name='available_rooms', )

    def get_available_rooms(self, qs, *args) -> QuerySet:
        """
        A method to filter available rooms based on check-in and check-out query params.
        Firstly we check if check-in param is in the request. If it is convert
        string to a datetime object - otherwise, set today's date as the check-in date.
        Then try to parse check-out date, but if it is not found, set check-in + 1 day as the default value.
        """
        checkin = self.request.query_params.get('checkin', date.today())
        if isinstance(checkin, str):
            checkin = datetime.strptime(checkin, '%Y-%m-%d').date()

        checkout = self.request.query_params.get('checkout', checkin + timedelta(days=1))
        if isinstance(checkout, str):
            checkout = datetime.strptime(checkout, '%Y-%m-%d').date()

        if checkin == checkout:
            raise ValidationError('checkout date can not be equal to checkin date')
        elif checkin > checkout:
            raise ValidationError('checkin date cant be lower than checkout date')

        booked_rooms_ids = Booking.objects.get_intersections(checkin, checkout).values('room')
        if booked_rooms_ids:
            qs = qs.exclude(id__in=booked_rooms_ids)
        return qs

    order_by = django_filters.OrderingFilter(
        fields=(
            ('price', 'price'),
            ('spots', 'spots'),
        ),
        field_labels={
            'price': 'Цена',
            'spots': 'Количество мест',
        }
    )

    class Meta:
        model = Room
        fields = ['price_gte', 'price_lte', 'spots_gte', 'spots_lte']
