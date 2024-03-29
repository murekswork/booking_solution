import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q

from rooms.models import Room


class BookingQuerySet(models.QuerySet):

    def get_intersections(self, checkin, checkout, room=None):
        """Method takes dates and room and checks for intersection in selected date"""
        lookup = (
            Q(checkin__lt=checkout) & Q(checkout__gt=checkin)) | (
            Q(checkin=checkin) & Q(checkout__gt=checkin)) | (
            Q(checkin__lt=checkout) & Q(checkout=checkout)
        )
        qs = self
        if room:
            qs = self.filter(room=room)
        qs = qs.filter(lookup)
        logging.warning(qs)
        return qs


class BookingManager(models.Manager):

    def get_queryset(self):
        return BookingQuerySet(self.model, using=self._db)

    def get_intersections(self, checkin, checkout, room=None):
        active_bookings = self.get_queryset().filter(active=True)
        return active_bookings.get_intersections(checkin, checkout, room)


class Booking(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='Бронирующий пользователь'
    )
    room = models.ForeignKey(
        Room, null=True, verbose_name='Забронированная комната', related_name='bookings', on_delete=models.CASCADE
    )
    checkin = models.DateField(
        verbose_name='Дата начала брони', db_index=True
    )
    checkout = models.DateField(
        verbose_name='Дата конца брони', db_index=True
    )
    active = models.BooleanField(
        default=True
    )
    objects = BookingManager()

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
        constraints = [
            models.CheckConstraint(
                check=Q(checkout__gt=F('checkin')),
                name='checkin_before_checkout'
            )
        ]

    def __str__(self):
        return f'{self.checkin} - {self.checkout}'

    def clean(self):
        super().clean()
        existing_bookings = Booking.objects.get_intersections(self.checkin, self.checkout, self.room).exclude(
            id=self.id)
        if existing_bookings.all():
            raise ValidationError('Выбранная дата уже занята!')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)