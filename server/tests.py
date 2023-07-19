from django.test import TestCase
from server.models import Menu
from decimal import Decimal

class MenuTest(TestCase):
    def setUp(self) -> None:
        self.item1 = Menu.objects.create(
            title = 'Pizza',
            price = 12.99,
            inventory = 10
        )

    def test_create_menu_item(self) -> None:
        item2 = Menu.objects.create(
            title = 'Burger',
            price = 17.99,
            inventory = 5
        )
        self.assertEqual(Menu.objects.count(), 2)
        self.assertEqual(item2.title, 'Burger')
        self.assertEqual(item2.price, Decimal(17.99))
        self.assertEqual(item2.inventory, 5)

    def test_get_menu_item(self) -> None:
        item = Menu.objects.get(id = self.item1.id)
        self.assertEqual(item.title, 'Pizza')
        self.assertEqual(item.price, Decimal(12.99).quantize(Decimal("0.00")))
        self.assertEqual(item.inventory, 10)

    def test_delete_menu_item(self) -> None:
        item = Menu.objects.get(id = self.item1.id)
        item.delete()
        self.assertEqual(Menu.objects.count(), 0)
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
import json

from server.models import Booking
from server.serializers import BookingSerializer

class BookingViewSetTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)

        self.booking1 = Booking.objects.create(
            first_name = 'XXXXXXXX',
            last_name = 'XXXXXXXX',
            email = 'XXXXXXXXXX@XXXXXXXXXXX.org',
            phone_number = '5555555555',
            people = 2,
            date = timezone.now().date(),
            time = '12:00'
        )
        self.booking2 = Booking.objects.create(
            first_name = 'XXXXXXXXd',
            last_name = 'XXXXXXXXXgd',
            email = 'XXXXXXXXXXXXXXX@XXXXXXXXXXXXX.goh',
            phone_number = '5555555554',
            people = 1,
            date = timezone.now().date(),
            time = '12:00'
        )
        self.valid_payload = {
            'first_name': 'Test User',
            'last_name': 'Test User',
            'email': 'XXXXX@XXXXXXXX.com',
            'phone_number': '5555555555',
            'people': 3,
            'date': timezone.now().date(),
            'time': '12:00',
        }
        self.invalid_payload = {
            'first_name': '',
            'last_name': '',
            'email': 'XXXXXXXXXXXXX',
            'phone_number': 'XXXXXXXXXXXXX',
            'people': 0,
            'date': timezone.now(),
            'time': '12:60',
        }

    def test_get_all_bookings(self):
        response = self.client.get(reverse('booking-list'))
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_booking(self) -> None:
        response = self.client.post(
            reverse('booking-list'),
            data = json.dumps(self.valid_payload, cls=DjangoJSONEncoder),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_booking(self) -> None:
        response = self.client.post(
            reverse('booking-list'),
            data = json.dumps(self.invalid_payload, cls=DjangoJSONEncoder),
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_valid_single_booking(self) -> None:
        response = self.client.get(reverse('booking-detail', kwargs={'pk': self.booking1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        booking = Booking.objects.get(pk=self.booking1.pk)
        serializer = BookingSerializer(booking)
        self.assertEqual(response.data, serializer.data)
        from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from server.models import Menu
from server.serializers import MenuSerializer

class MenuViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        self.pizza = Menu.objects.create(title='Pizza', price=12.99, inventory=10)
        self.burger = Menu.objects.create(title='Burger', price=8.99, inventory=5)
        self.pasta = Menu.objects.create(title='Pasta', price=15.99, inventory=7)
    
    def loginAsTestUser(self) -> None:
        self.client.login(username='testuser', password='testpassword')
    
    def test_view_authentication(self) -> None:
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.loginAsTestUser()
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_getall(self):
        self.loginAsTestUser()
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        menu = Menu.objects.all()
        serializer = MenuSerializer(menu, many=True)
        self.assertEqual(response.data, serializer.data)