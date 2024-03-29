from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rooms.models import Room


class RoomsListAPIViewTestCase(TestCase):

    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval('rooms_room_id_seq', 1, false)")
            cursor.execute("SELECT setval('rooms_room_id_seq', 1, false)")

        self.user = get_user_model().objects.create_user(username='user', email='user@email.com')
        self.room1 = Room.objects.create(room_type=1, spots=1, price=1000)
        self.room2 = Room.objects.create(room_type=2, spots=2, price=2000)
        self.room3 = Room.objects.create(room_type=3, spots=3, price=3000)
        self.room4 = Room.objects.create(room_type=4, spots=4, price=4000)
        self.expected_data = {'count': 4, 'next': None, 'previous': None,
                              'results': [{'id': 1, 'room_type': 1, 'spots': 1, 'price': '1000.00'},
                                          {'id': 2, 'room_type': 2, 'spots': 2, 'price': '2000.00'},
                                          {'id': 3, 'room_type': 3, 'spots': 3, 'price': '3000.00'},
                                          {'id': 4, 'room_type': 4, 'spots': 4, 'price': '4000.00'}]}

    def test_not_authenticated_user_can_see_rooms(self):
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.expected_data)

    def test_authenticated_user_can_see_rooms(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rooms'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.expected_data)

    def test_view_sort_by_price(self):
        response = self.client.get(reverse('rooms') + '?order_by=price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], self.expected_data['results'])

    def test_view_sort_by_price_desc(self):
        response = self.client.get(reverse('rooms') + '?order_by=-price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], self.expected_data['results'][::-1])

    def test_view_sort_by_spots(self):
        response = self.client.get(reverse('rooms') + '?order_by=spots')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.expected_data)

    def test_view_sort_by_spots_desc(self):
        response = self.client.get(reverse('rooms') + '?order_by=-spots')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], self.expected_data['results'][::-1])

    def test_view_filter_by_price_gte(self):
        response = self.client.get(reverse('rooms') + '?price_gte=2000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], list(self.expected_data['results'][1:]))

    def test_view_filter_by_price_lte(self):
        response = self.client.get(reverse('rooms') + '?price_lte=2001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], list(self.expected_data['results'][:2]))

    def test_view_filter_by_spots_gte(self):
        response = self.client.get(reverse('rooms') + '?spots_gte=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], list(self.expected_data['results'][1:]))

    def test_view_filter_by_spots_lte(self):
        response = self.client.get(reverse('rooms') + '?spots_lte=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['results'], list(self.expected_data['results'][:1]))

    def test_view_filter_by_spots_and_sort_by_price_desc(self):
        response = self.client.get(reverse('rooms') + '?spots_gte=3&order_by=-price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = (list(self.expected_data['results'][2::]))
        expected.reverse()
        self.assertEqual(response.json()['results'], expected)

    def test_view_filter_by_spots_and_sort_by_price(self):
        response = self.client.get(reverse('rooms') + '?spots_gte=3&order_by=price')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = (list(self.expected_data['results'][2::]))
        self.assertEqual(response.json()['results'], expected)

    def test_view_filter_by_price_and_sort_by_spots(self):
        response = self.client.get(reverse('rooms') + '?price_gte=3000&order_by=spots')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = (list(self.expected_data['results'][2::]))
        self.assertEqual(response.json()['results'], expected)

    def test_view_filter_by_price_and_sort_by_spots_desc(self):
        response = self.client.get(reverse('rooms') + '?price_gte=3000&order_by=-spots')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected = (list(self.expected_data['results'][2::]))
        expected.reverse()
        self.assertEqual(response.json()['results'], expected)
