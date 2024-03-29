import datetime

from django.core.exceptions import ValidationError
from django.db import models


class Room(models.Model):
    class RoomTypeChoices(models.IntegerChoices):
        ECONOMIC = 1, 'ECONOMIC'
        STANDARD = 2, 'STANDARD'
        PREMIUM = 3, 'PREMIUM'
        LUXURY = 4, 'LUXURY'

    room_type = models.IntegerField(choices=RoomTypeChoices, blank=False, null=False, verbose_name='Тип комнаты')
    spots = models.IntegerField(blank=False, null=False, verbose_name='Количество мест')
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False, verbose_name='Цена за день', db_index=True)

    def __str__(self):
        return f'Номер {self.room_type} класса на {self.spots} мест'

    def delete(self, using=None, keep_parents=False):
        active_bookings = self.bookings.filter(active=True, checkout__gt=datetime.date.today())
        if active_bookings.exists():
            raise ValidationError('Нельзя удалить комнаты брони которых активны и дата выезда больше текущей!')
        super().delete(using, keep_parents)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'
