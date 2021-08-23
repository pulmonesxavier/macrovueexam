from rest_framework.test import APITestCase
from rest_framework import status
from unittest import expectedFailure
from django.contrib.auth.models import User


class BaseTest(APITestCase):
    def setUp(self):

        self.base_user = User.objects.create_user('macrovue', 'test@test.com', 'pass123')

    @expectedFailure
    def test_create_user(self):
        """
        Test a successful user creation.
        """
        data = {
            'username': 'xavier',
            'email': 'xavier@xavier.com',
            'password': 'xavierpass'
        }

        res = self.client.post('api/auth/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['email'], data['email'])
        self.assertIsNotNone(User.objects.get(email='xavier@xavier.com'))
