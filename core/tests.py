from rest_framework.test import APITestCase
from rest_framework import status
from unittest import expectedFailure
from django.contrib.auth.models import User


class BaseTest(APITestCase):
    def setUp(self):

        self.base_user = User.objects.create_user('macrovue', 'test@test.com', 'pass123')

    def test_create_user(self):
        """
        Test a successful user creation.
        """
        data = {
            'username': 'xavier',
            'email': 'xavier@xavier.com',
            'password': 'xavierpass'
        }

        res = self.client.post('/users/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['email'], data['email'])
        self.assertIsNotNone(User.objects.get(email='xavier@xavier.com'))

    def test_email_taken_user(self):
        """
        Test if email is already taken
        """
        data = {
            'username': 'xavier',
            'email': 'test@test.com',
            'password': 'xavierpass'
        }
        res = self.client.post('/users/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_taken_user(self):
        """
        Test if username is already taken
        """
        data = {
            'username': 'macrovue',
            'email': 'test@test2.com',
            'password': 'xavierpass'
        }
        res = self.client.post('/users/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_short_user(self):
        """
        Test if password  is less than 6 characters
        """
        data = {
            'username': 'macrovue',
            'email': 'test@test2.com',
            'password': 'xavi'
        }
        res = self.client.post('/users/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_empty_user(self):
        """
        Test if no data is passed
        """
        data = {}
        res = self.client.post('/users/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_login_success_user(self):
        """
        Test for successful user login
        """
        data = {
            'username': 'macrovue',
            'password': 'pass123'
        }
        res = self.client.post('/login/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)

    def test_login_wrong_credentials_user(self):
        """
        Test if wrong credentials
        """
        data = {
            'username': 'macrovu2e',
            'password': 'pass123'
        }
        res = self.client.post('/login/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_success_user(self):
        """
        Test successful logout for the user
        """
        data = {
            'username': 'macrovue',
            'password': 'pass123'
        }
        self.client.post('/login/', data=data, format='json')
        res = self.client.get('/logout/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_logout_unauthorized_user(self):
        """
        Test successful logout for the user
        """
        data = {
            'username': 'macrovue',
            'password': 'pass123'
        }
        res = self.client.get('/logout/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
