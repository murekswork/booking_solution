import datetime
from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection
from django.test import TestCase

from booking.models import Booking
from rooms.models import Room


class BookingModelTestCase(TestCase):

    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval('rooms_room_id_seq', 1, false)")
            cursor.execute("SELECT setval('rooms_room_id_seq', 1, false)")
        self.room = Room.objects.create(room_type=1, price=2500.2, spots=3)
        self.user = get_user_model().objects.create(username='test_user', email='test@mail.com')
        self.booking = Booking.objects.create(user=self.user, room=self.room, checkin=date(2024, 3, 5),
                                              checkout=date(2024, 3, 8), active=True)

    def test_booking_model_field_id(self):
        self.assertTrue(self.booking.id)

    def test_booking_model_field_checkin(self):
        self.assertEqual(self.booking.checkin, date(2024, 3, 5))

    def test_booking_model_field_checkout(self):
        self.assertEqual(self.booking.checkout, date(2024, 3, 8))

    def test_booking_model_field_user(self):
        self.assertEqual(self.booking.user, self.user)

    def test_booking_model_field_room(self):
        self.assertEqual(self.booking.room_id, 1)

    def test_booking_model_when_checkin_earlier_than_checkout_then_raise_error(self):
        with self.assertRaises(IntegrityError):
            Booking.objects.create(room=self.room, checkin=date(2024, 3, 10), checkout=date(2024, 3, 9))

    def test_booking_model_save_when_date_already_booked_then_raise_error(self):
        user2 = get_user_model().objects.create_user(username='test1', email='test1@email.com')
        with self.assertRaises(ValidationError):
            Booking.objects.create(user=user2, room=self.room, checkin=date(2024, 3, 6),
                                   checkout=date(2024, 3, 15), active=True)

    def test_booking_model_save_when_date_is_free(self):
        b = Booking.objects.create(room=self.room, checkin=date(2024, 3, 9),
                                   checkout=date(2024, 3, 11))
        self.assertFalse(b == ValidationError)

    def test_booking_model_save_when_invalid_room_then_raise_error(self):
        with self.assertRaises(ValidationError):
            Booking.objects.create(room=self.room, checkin=date(2024, 3, 5),
                                   checkout=date(2024, 3, 8))

    def test_booking_model_save_when_invalid_date_then_raise_error(self):
        with self.assertRaises(ValidationError):
            Booking.objects.create(room=self.room, checkin='2024-03-1041',
                                   checkout=datetime.datetime.now() + datetime.timedelta(days=3))

    def test_booking_model_status_can_be_updated_when_checkout_time_came(self):
        self.booking.checkin = date.today() - datetime.timedelta(days=2)
        self.booking.checkout = date.today()
        self.booking.save()
        self.booking.status = 0
        self.booking.save()
        self.assertEqual(self.booking.status, 0)


class BookingManagerTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', email='test@email.com')
        self.room = Room.objects.create(room_type=1, price=2500, spots=5)
        self.booking = Booking.objects.create(room=self.room, user=self.user, checkin=date.today(),
                                              checkout=date.today() + datetime.timedelta(days=7))

    def test_manager_get_intersections_method_when_checkin_between_existing_checkin_and_checkout(self):
        checkin = date.today() + datetime.timedelta(days=2)
        checkout = date.today() + datetime.timedelta(days=10)
        intersections = Booking.objects.get_intersections(checkin, checkout, self.room)
        self.assertEqual(len(intersections), 1)

    def test_manager_get_intersections_method_when_checkout_between_existing_checkin_and_checkout(self):
        checkin = date.today() - datetime.timedelta(days=2)
        checkout = date.today() + datetime.timedelta(days=2)
        print(checkin, checkout)
        intersections = Booking.objects.get_intersections(checkin, checkout, self.room)
        self.assertEqual(len(intersections), 1)

    def test_manager_get_intersections_method_when_checkin_equal_to_existing_checkin_then_true(self):
        checkin = date.today()
        checkout = date.today() + datetime.timedelta(days=15)
        intersections = Booking.objects.get_intersections(checkin, checkout, self.room)
        self.assertEqual(len(intersections), 1)

    def test_manager_get_intersections_method_when_checkin_equal_to_existing_checkout_then_false(self):
        checkin = date.today() + datetime.timedelta(days=7)
        checkout = date.today() + datetime.timedelta(days=10)
        intersections = Booking.objects.get_intersections(checkin, checkout, self.room)
        self.assertEqual(len(intersections), 0)

    def test_manager_get_intersections_method_when_checkout_equal_to_existing_checkin(self):
        checkin = date.today() - datetime.timedelta(days=7)
        checkout = date.today()
        intersections = Booking.objects.get_intersections(checkin, checkout, self.room)
        self.assertEqual(len(intersections), 0)

    def test_manager_get_intersections_method_when_equal_dates(self):
        checkin = date.today()
        checkout = date.today() + datetime.timedelta(days=7)
        intersections = Booking.objects.get_intersections(checkin, checkout, self.room)
        self.assertEqual(len(intersections), 1)
