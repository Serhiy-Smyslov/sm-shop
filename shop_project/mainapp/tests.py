from decimal import Decimal
from unittest import mock

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Category, Laptop, Smartphone, Cart, Customer, CartProduct
from .views import recalc_cart, AddView, BaseView

# Create your tests here.
User = get_user_model()


class ShopTestCases(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')
        self.category = Category.objects.create(name='Laptop', slug='laptop')
        image = SimpleUploadedFile('Знімок_екрана_2021-05-18_о_10_05_53.png', content=b'', content_type='image/png')
        self.laptop = Laptop.objects.create(
            category=self.category,
            title='Test Laptop',
            slug='test-slug',
            image=image,
            price=Decimal('50000.00'),
            diagonal='13.3',
            display_type='IPS',
            processor_freq='1Gz',
            ram='6 GB',
            video='GeForse GTX',
            time_without_charge='10 hours'
        )
        self.customer = Customer.objects.create(user=self.user, phone='1111111111', address='Streat')
        self.cart = Cart.objects.create(owner=self.customer)
        self.cart_product = CartProduct.objects.create(
            user=self.customer,
            cart=self.cart,
            content_object=self.laptop
        )

    def test_add_to_cart(self):
        self.cart.objects.add(self.cart_product)
        recalc_cart(self.cart)
        self.assertIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.products.count, 1)
        self.assertEqual(self.cart.final_price, '50000.00')

    def test_response_from_add_to_cart_view(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        response = AddView.as_view()(request, ct_model='laptop', slug='test-slug')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cart/')

    def test_mock_homepage(self):
        mock_data = mock.Mock(status_code=444)
        with mock.patch('mainapp.views.BaseView.get', return_value=mock_data) as mock_data_:
            factory = RequestFactory()
            request = factory.get()
            request.user = self.user
            response = BaseView.as_view()(request)
            self.assertEqual(response.status_code, 444)
