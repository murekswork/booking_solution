import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from booking.models import Booking
from rooms.models import Room


class RoomModelTestCase(TestCase):

    def setUp(self):
        self.room = Room.objects.create(room_type=1, price=2500, spots=3)

    def test_room_model_field_room_type(self):
        self.assertEqual(self.room.room_type, 1)

    def test_room_model_field_price(self):
        self.assertEqual(self.room.price, 2500)

    def test_room_model_field_spots(self):
        self.assertEqual(self.room.spots, 3)

    def test_room_model_field_price_when_price_decimal(self):
        self.room.price = Decimal(3333.33)
        self.room.save()
        self.assertEqual(self.room.price, Decimal(3333.33))


class TestRoomModelDeleteTestCase(TestCase):

    def setUp(self):
        self.room = Room.objects.create(room_type=1, price=2500, spots=3)
        self.user = get_user_model().objects.create(username='user', email='email@mail.com')

    def test_room_manager_delete_room_when_active_booking_in_future_then_raise_error(self):
        Booking.objects.create(room=self.room,
                               checkin=datetime.date.today(),
                               checkout=datetime.date.today() + datetime.timedelta(days=3),
                               user=self.user)
        with self.assertRaises(ValidationError):
            self.room.delete()

    def test_room_manager_delete_room_when_active_booking_in_past_then_ok(self):
        # TODO: REMAKE THIS
        Booking.objects.create(room=self.room,
                               checkin=datetime.date.today() - datetime.timedelta(days=5),
                               checkout=datetime.date.today() - datetime.timedelta(days=3),
                               user=self.user)
        assert self.room.delete != ValidationError

    def test_room_manager_delete_room_when_not_active_booking_in_future_then_ok(self):
        Booking.objects.create(room=self.room,
                               checkin=datetime.date.today(),
                               checkout=datetime.date.today() + datetime.timedelta(days=3),
                               user=self.user,
                               active=False)
        assert self.room.delete != ValidationError
