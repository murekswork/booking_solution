from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTestCase(TestCase):

    def setUp(self):
        self.simple_user = get_user_model().objects.create_user(username='test', email='email@email.com')
        self.super_user = get_user_model().objects.create_superuser(username='admin', email='admin@admin.com')
        self.simple_user.set_password('strong1123.')
        self.super_user.set_password('superadmin1123')

    def test_custom_user_str(self):
        self.assertEqual(self.simple_user.__str__(), 'test')
        self.assertEqual(self.super_user.__str__(), 'admin')

    def test_custom_user_username(self):
        self.assertEqual(self.simple_user.username, 'test')
        self.assertEqual(self.super_user.username, 'admin')

    def test_custom_user_email(self):
        self.assertEqual(self.simple_user.email, 'email@email.com')
        self.assertEqual(self.super_user.email, 'admin@admin.com')

    def test_custom_user_password_hashed(self):
        self.assertNotEqual(self.simple_user, 'strong1123.')
        self.assertNotEqual(self.super_user, 'superadmin1123.')

    def test_custom_user_is_superuser(self):
        self.assertFalse(self.simple_user.is_superuser)
        self.assertTrue(self.super_user.is_superuser)
