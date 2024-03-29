from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rooms.models import Room


class TestSignupAPIView(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test213', email='test213@email.com')
        self.user.set_password('test123321')
        self.user.save()

    def test_login_api_view(self):
        response = self.client.post(reverse('login'), data={'username': 'test213', 'password': 'test123321'},
                                    content_type='application/json')
        print(response)
        print(response.json())

    def test_signup_api_view_when_valid_credentials_then_200(self):
        response = self.client.post(reverse('signup'),
                                    data={'username': 'test111', 'password': 'test111', 'email': 'test111@email.com'})
        self.assertEqual(response.status_code, 201)
        print(response)
        print(response.json())

    def test_signup_api_view_with_existing_username_then_400(self):
        response = self.client.post(reverse('signup'),
                                    data={'username': 'test213', 'password': 'test111', 'email': 'test111@email.com'})
        print(response, response.json())
        self.assertEqual(response.status_code, 400)

    def test_signup_api_view_with_existing_email_then_400(self):
        response = self.client.post(reverse('signup'),
                                    data={'username': 'test2132', 'password': 'test111', 'email': 'test213@email.com'})
        print(response, response.json())
        self.assertEqual(response.status_code, 400)

    def test_signup_api_view_when_logged_in_then_403(self):
        login_response = self.client.post(reverse('login'),
                                          data={'username': self.user.username, 'password': 'test123321'})
        self.assertEqual(login_response.status_code, 200)
        response = self.client.post(reverse('signup'),
                                    data={'username': 'test111', 'password': 'test111', 'email': 'test111@email.com'})
        self.assertEqual(response.status_code, 403)

    def test_signup_api_view_user_can_login(self):
        response = self.client.post(reverse('signup'),
                                    data={'username': 'test111', 'password': 'test111', 'email': 'test111@email.com'})
        self.assertEqual(response.status_code, 201)
        login_response = self.client.post(reverse('login'), data={'username': 'test111', 'password': 'test111'})
        self.assertEqual(login_response.status_code, 200)


class TestLoginApiViewTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test1', email='test1@email.com')
        self.user.set_password('test1')
        self.user.save()

    def test_login_api_view_when_invalid_creds(self):
        login_response = self.client.post(reverse('login'), data={'username': 'test11', 'password': 'test1'})
        self.assertEqual(login_response.status_code, 400)
        self.assertEqual(login_response.json(), {'detail': 'invalid credentials'})

    def test_login_api_view_when_valid_creds(self):
        login_response = self.client.post(reverse('login'), data={'username': 'test1', 'password': 'test1'})
        self.assertEqual(login_response.status_code, 200)

    def test_login_api_view_when_valid_creds_return_token(self):
        login_response = self.client.post(reverse('login'), data={'username': 'test1', 'password': 'test1'})
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue('token' in login_response.json())

    def test_login_api_view_access_to_auth_required_pages_when_auth_with_token(self):
        room = Room.objects.create(price=2500, room_type=1, spots=3)
        token = self.client.post(reverse('login'), data={'username': 'test1', 'password': 'test1'}).json()['token']
        self.client.logout()
        response = self.client.post(reverse('booking-create'), data={'room': room.id,
                                                                     'checkin': '2024-03-29',
                                                                     'checkout': '2024-04-29'
                                                                     }, headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(response.status_code, 201)

    def test_login_api_view_access_to_auth_required_pages_when_auth_with_session(self):
        room = Room.objects.create(price=2500, room_type=1, spots=3)
        token = self.client.post(reverse('login'), data={'username': 'test1', 'password': 'test1'}).json()['token']
        response = self.client.post(reverse('booking-create'), data={'room': room.id,
                                                                     'checkin': '2024-03-29',
                                                                     'checkout': '2024-04-29'
                                                                     }, headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(response.status_code, 201)
