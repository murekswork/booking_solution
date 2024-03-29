from datetime import date, datetime

import django_filters

from booking.models import Booking
from rooms.models import Room


class RoomFilter(django_filters.FilterSet):
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    spots_gte = django_filters.NumberFilter(field_name='spots', lookup_expr='gte')
    spots_lte = django_filters.NumberFilter(field_name='spots', lookup_expr='lte')

    checkin = django_filters.DateFilter(method='get_available_rooms', field_name='available_rooms', )
    checkout = django_filters.DateFilter(method='get_available_rooms', field_name='available_rooms', )

    def get_available_rooms(self, qs, *args):
        checkin = self.request.query_params.get('checkin', date.today())
        checkout = self.request.query_params.get('checkout', date.today())
        if isinstance(checkin, str):
            checkin = datetime.strptime(checkin, '%Y-%m-%d').date()
        if isinstance(checkout, str):
            checkout = datetime.strptime(checkout, '%Y-%m-%d').date()
        booked_ids = Booking.objects.get_intersections(checkin, checkout).values('room')
        if booked_ids:
            qs = qs.exclude(id__in=booked_ids)
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
