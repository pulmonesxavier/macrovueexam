from rest_framework.test import APITestCase
from rest_framework import status
from unittest import expectedFailure
from django.contrib.auth.models import User

from core.models import Order, Stock


class BaseTest(APITestCase):
    def setUp(self):

        self.base_user = User.objects.create_user(
            'macrovue',
            'test@test.com',
            'pass123'
        )
        self.super_user = User.objects.create_superuser(
            'supermacrovue',
            'supertest@test.com',
            'superpass123'
        )
        self.base_stock = Stock.objects.create(
            name='Sample Stock',
            price='1.0'
        )
        self.base_order = Order.objects.create(
            owner=self.base_user,
            stock=self.base_stock,
            type=1,
            quantity=100
        )


class AuthenticationTests(BaseTest):
    """
    Tests for Authentication functionality
    """
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


class StockTests(BaseTest):
    """
    Tests for Stock Functionalities
    """
    def test_stock_create_admin(self):
        """
        Test a successful stock creation.
        """
        data = {
            'name': 'xavier',
            'price': '1.2',
        }

        self.client.login(username=self.super_user.username, password='superpass123')
        res = self.client.post('/stocks/', data=data, format='json')
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['name'], data['name'])
        self.assertIsNotNone(Stock.objects.get(id=res.data['id']))

    def test_stock_create_unauthorized_admin(self):
        """
        Test an unauthorized stock creation.
        """
        data = {
            'name': 'xavier',
            'price': '1.2',
        }

        self.client.login(username=self.base_user.username, password='pass123')
        res = self.client.post('/stocks/', data=data, format='json')
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_stock_create_empty_admin(self):
        """
        Test an empty stock creation.
        """
        data = {
            'name': '',
            'price': '',
        }

        self.client.login(username=self.super_user.username, password='superpass123')
        res = self.client.post('/stocks/', data=data, format='json')
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_stock_list_success(self):
        """
        Test for successful stock list
        """
        res = self.client.get('/stocks/', format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_stock_list_search_success(self):
        """
        Test for successful searching of stock
        """
        test_stock = Stock.objects.create(
            name='Xavier',
            price='3.24'
        )

        res = self.client.get('/stocks/?search=Xavier', format='json')
        
        self.assertContains(res, test_stock.name)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_stock_retrieve_success(self):
        """
        Test for successful stock list
        """
        res = self.client.get(f'/stocks/{self.base_stock.id}/', format='json')
        
        self.assertEqual(res.data['name'], self.base_stock.name)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_retrieve_total_invested(self):
        for x in range(1, 10):
            Order.objects.create(
                owner=self.base_user,
                stock=self.base_stock,
                type=1,
                quantity=100
            )
        data = {
            'owner': self.base_user.id,
            'stock': self.base_stock.id,
        }
        res = self.client.post('/total-invested/', data=data, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['total_invested'], self.base_stock.get_total_invested(self.base_user))

class OrderTests(BaseTest):
    """
    Tests for Order functionalities
    """
    def test_order_authentication(self):
        """
        Test for order authentication
        """
        data = {
            'owner': self.base_user.id,
            'stock': self.base_stock.id,
            'type': 1,
            'quantity': 100
        }
        res = self.client.post('/orders/')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_order_create_success(self):
        """
        Test for order creation
        """
        data = {
            'owner': self.base_user.id,
            'stock': self.base_stock.id,
            'type': 1,
            'quantity': 100
        }
        self.client.login(username=self.base_user.username, password='pass123')
        res = self.client.post('/orders/', data=data, format='json' )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_order_create_forbidden(self):
        """
        Test for order creation
        """
        data = {
            'owner': self.super_user.id,
            'stock': self.base_stock.id,
            'type': 1,
            'quantity': 100
        }
        self.client.login(username=self.base_user.username, password='pass123')
        res = self.client.post('/orders/', data=data, format='json')
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_list_success(self):
        """
        Test for successful order list
        """
        self.client.login(username=self.base_user.username, password='pass123')
        res = self.client.get('/orders/', format='json')
        self.client.logout()

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_order_retrieve_success(self):
        """
        Test for successful order retrieve
        """
        self.client.login(username=self.base_user.username, password='pass123')
        res = self.client.get(f'/orders/{self.base_order.id}/', format='json')
        self.client.logout()

        self.assertEqual(res.data['id'], self.base_order.id)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
