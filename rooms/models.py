import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Room(models.Model):
    ROOM_TYPES_CHOICES = (
        (1, 'Эконом'),
        (2, 'Стандарт'),
        (3, 'Премиум'),
        (4, 'Люкс')
    )

    room_type = models.IntegerField(choices=ROOM_TYPES_CHOICES, blank=False, null=False, verbose_name='Тип комнаты')
    spots = models.IntegerField(blank=False, null=False, verbose_name='Количество мест')
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, verbose_name='Цена за день')

    def delete(self, using=None, keep_parents=False):
        active_bookings = self.bookings.filter(Q(active=True) & Q(checkout__gt=datetime.date.today()))
        if active_bookings.exists():
            raise ValidationError('Нельзя удалить комнаты брони которых активны и дата выезда больше текущей!')
        super().delete(using, keep_parents)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
