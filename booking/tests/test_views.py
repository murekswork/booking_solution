from datetime import date

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.urls import reverse

from booking.models import Booking
from rooms.models import Room


class TestListCreateBookingViewTestCaseSetupMixin(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', email='test')
        self.room = Room.objects.create(price=1000, room_type=1, spots=1)
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval('rooms_room_id_seq', 1, false)")
            cursor.execute("SELECT setval('rooms_room_id_seq', 1, false)")


class TestListCreateBookingViewPost(TestListCreateBookingViewTestCaseSetupMixin):

    def test_view_not_authenticated_user_create_booking_then_raise_403(self):
        response = self.client.post(reverse('booking-create'),
                                    data={'room': self.room.id, 'checkin': '2024-03-29', 'checkout': '2024-04-03'})
        self.assertEqual(response.status_code, 403)

    def test_view_authenticated_user_create_booking_then_201(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('booking-create'),
                                    data={'room': self.room.id, 'checkin': '2024-03-29', 'checkout': '2024-04-03'})
        self.assertEqual(response.status_code, 201)

    def test_view_authenticated_user_create_booking_with_checkin_inside_existing_date_raise_409(self):
        self.client.force_login(self.user)
        Booking.objects.create(room=self.room, checkin=date(2024, 3, 28),
                               checkout=date(2024, 3, 30))
        response = self.client.post(reverse('booking-create'),
                                    data={'room': self.room.id, 'checkin': '2024-03-29', 'checkout': '2024-04-03'})
        self.assertEqual(response.status_code, 409)

    def test_view_authenticated_user_create_booking_with_checkout_inside_existing_date_raise_409(self):
        self.client.force_login(self.user)
        Booking.objects.create(room=self.room, checkin=date(2024, 3, 28),
                               checkout=date(2024, 3, 30))
        response = self.client.post(reverse('booking-create'),
                                    data={'room': self.room.id, 'checkin': '2024-03-25', 'checkout': '2024-03-29'})
        self.assertEqual(response.status_code, 409)

    def test_view_authenticated_user_create_booking_with_date_inside_existing_date_raise_409(self):
        self.client.force_login(self.user)
        Booking.objects.create(room=self.room, checkin=date(2024, 3, 20),
                               checkout=date(2024, 3, 30))
        response = self.client.post(reverse('booking-create'),
                                    data={'room': self.room.id, 'checkin': '2024-03-25', 'checkout': '2024-03-26'})
        self.assertEqual(response.status_code, 409)

    def test_view_authenticated_user_create_booking_with_existing_date_inside_date_raise_409(self):
        self.client.force_login(self.user)
        Booking.objects.create(room=self.room, checkin=date(2024, 3, 25),
                               checkout=date(2024, 3, 26))
        response = self.client.post(reverse('booking-create'),
                                    data={'room': self.room.id, 'checkin': '2024-03-20', 'checkout': '2024-03-30'})
        self.assertEqual(response.status_code, 409)


class TestListCreateBookingViewGet(TestListCreateBookingViewTestCaseSetupMixin):

    def test_view_not_authenticated_user_booking_list_then_raise_403(self):
        response = self.client.get(reverse('booking-my'))
        self.assertEqual(response.status_code, 403)

    def test_view_authenticated_user_booking_list_then_200(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('booking-my'))
        self.assertEqual(response.status_code, 200)

    def test_view_authenticated_user_booking_list_with_one_active_booking(self):
        Booking.objects.create(room=self.room, checkin=date(2024, 3, 20),
                               checkout=date(2024, 3, 30), user=self.user)
        self.client.force_login(self.user)
        response = self.client.get(reverse('booking-my'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         [{'room': 1, 'checkin': '2024-03-20', 'checkout': '2024-03-30', 'active': True}])

    def test_view_authenticated_user_booking_list_with_not_active_booking(self):
        Booking.objects.create(room=self.room, checkin=date(2024, 3, 20),
                               checkout=date(2024, 3, 30), user=self.user, active=False)
        self.client.force_login(self.user)
        response = self.client.get(reverse('booking-my'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         [{'room': 1, 'checkin': '2024-03-20', 'checkout': '2024-03-30', 'active': False}])


class BookingRetrieveUpdateAPIViewTestCaseSetupMixin(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', email='test')
        self.room = Room.objects.create(price=1000, room_type=1, spots=1)
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval('rooms_room_id_seq', 1, false)")
            cursor.execute("SELECT setval('rooms_room_id_seq', 1, false)")
        self.booking = Booking.objects.create(room=self.room, checkin=date(2024, 3, 20),
                                              checkout=date(2024, 3, 30), user=self.user, active=True)


class BookingRetrieveUpdateAPIViewRetrieveTestCase(BookingRetrieveUpdateAPIViewTestCaseSetupMixin):

    def test_not_authenticated_user_cant_retrieve_any_booking(self):
        response = self.client.get(reverse('booking-detail', kwargs={'pk': self.booking.id}))
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_retrieve_his_booking(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('booking-detail', kwargs={'pk': self.booking.id}))
        self.assertEqual(response.status_code, 200)

    def test_superuser_can_retrieve_not_his_booking(self):
        superuser = get_user_model().objects.create_superuser('superuser', email='superuser@email.com')
        self.client.force_login(superuser)
        response = self.client.get(reverse('booking-detail', kwargs={'pk': self.booking.id}))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_cant_retrieve_not_his_booking(self):
        other_user = get_user_model().objects.create_user(username='test1', email='test1')
        other_booking = Booking.objects.create(room=self.room, checkin=date(2024, 5, 20),
                                               checkout=date(2024, 5, 30), user=other_user, active=True)
        self.client.force_login(self.user)
        response = self.client.get(reverse('booking-detail', kwargs={'pk': other_booking.id}))
        self.assertEqual(response.status_code, 404)


class BookingRetrieveUpdateAPIViewUpdateTestCase(BookingRetrieveUpdateAPIViewTestCaseSetupMixin):

    def test_not_authenticated_user_cant_patch_booking(self):
        response = self.client.patch(reverse('booking-update', kwargs={'pk': self.booking.id}),
                                     data={'active': False})
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_patch_his_booking(self):
        self.client.force_login(self.user)
        response = self.client.patch(reverse('booking-update', kwargs={'pk': self.booking.id}),
                                     data={'active': False}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_cant_patch_his_booking_with_invalid_data(self):
        self.client.force_login(self.user)
        response = self.client.patch(reverse('booking-update', kwargs={'pk': self.booking.id}),
                                     data={'active': 'Invalid data'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_authenticated_user_cant_patch_not_his_booking(self):
        self.client.force_login(self.user)
        other_user = get_user_model().objects.create_user(username='other_user', email='other_user@email.com')
        other_booking = Booking.objects.create(room=self.room, checkin=date(2024, 4, 20),
                                               checkout=date(2024, 4, 30), user=other_user, active=True)
        response = self.client.patch(reverse('booking-update', kwargs={'pk': other_booking.id}),
                                     data={'active': 'Invalid data'}, content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_super_user_can_patch_any_booking(self):
        superuser = get_user_model().objects.create_superuser(username='superuser', email='superuser@email')
        self.client.force_login(superuser)
        response = self.client.patch(reverse('booking-update', kwargs={'pk': self.booking.id}),
                                     data={'active': False}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_booking_changed_after_patch(self):
        self.client.force_login(self.user)
        response = self.client.patch(reverse('booking-update', kwargs={'pk': self.booking.id}),
                                     data={'active': False}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('booking-detail', kwargs={'pk': self.booking.id}))
        self.assertEqual(response.json()['active'], False)
