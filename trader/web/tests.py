from mock import call, patch

from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ValidationError

from web.models import TradeOrder

class HomepageTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_display_homepage(self):
		response = self.client.get('/')

		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'web/index.html')
		self.assertContains(response, 'Simple Trader - Homepage')

	def test_add_form_button_is_displayed(self):
		response = self.client.get('/')

		self.assertContains(response, 'Add new order')

	def test_list_trades_is_displayed(self):
		order = TradeOrder.objects.create(
			email='user@example.com', 
			amount=10,
			quality='normal'
		)

		response = self.client.get('/')

		self.assertContains(response, order.email)

		order.delete()

	@patch('web.views.requests')
	def test_api_price_unavailable_handled(self, mock_requests):
		mock_requests.get.return_value.status_code = 403
		
		response = self.client.get('/')

		self.assertContains(response, 'Unavailable')


	def tearDown(self):
		pass

class OrderAddTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_that_form_is_displayed(self):
		response = self.client.get('/add/')

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, '<form')
		self.assertContains(response, 'name="amount"')

	def test_that_correct_form_is_used(self):
		from web.forms import OrderAddForm
		
		response = self.client.get('/add/')
		self.assertIsInstance(response.context['form'], OrderAddForm)

	def test_form_add(self):
		data = {
			'email': 'user@example.com',
			'amount': 10,
			'quality': 'premium',
		}

		response = self.client.post('/add/', data)
		order = TradeOrder.objects.latest('id')

		self.assertRedirects(response, '/order/{0}/'.format(order.id))

		order.delete()

	def test_form_with_gmail_fails(self):
		data = {
			'email': 'user@gmail.com',
			'amount': 10,
			'quality': 'premium',
		}

		response = self.client.post('/add/', data)
		
		self.assertFormError(response, 'form', 'email', 'We do not allow gmail.com email addresses')

	def test_form_with_zero_amount(self):
		data = {
			'email': 'user@example.com',
			'amount': 0,
			'quality': 'premium',
		}

		response = self.client.post('/add/', data)

		self.assertContains(response, 'Order amount must be more than 0')

	def test_homepage_do_not_list_expired_order(self):
		TradeOrder.objects.create(
			email='expired@example.com', 
			amount=10,
			quality='normal',
			expired=True
		)

		TradeOrder.objects.create(
			email='active@example.com', 
			amount=10,
			quality='normal',
			expired=False
		)

		response = self.client.get('/')

		self.assertContains(response, 'active@example.com')
		self.assertNotContains(response, 'expired@example.com')


class OrderDetailTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_display_trade(self):
		order = TradeOrder.objects.create(
			email='user@example.com', 
			amount=10,
			quality='normal',
		)
		response = self.client.get('/order/{0}/'.format(order.id))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Order number: {0}'.format(order.id) )

		order.delete()

	def test_do_not_display_expired_order(self):
		order = TradeOrder.objects.create(
			email='expired@example.com', 
			amount=10,
			quality='normal',
			expired=True
		)

		response = self.client.get('/order/{0}/'.format(order.id))
		self.assertEquals(response.status_code, 404)

		order.delete()

	def tearDown(self):
		TradeOrder.objects.all().delete()

class TradeOrderModelTest(TestCase):

	def test_require_one_or_more_order_amount(self):
		
		with self.assertRaises(ValidationError):
			TradeOrder.objects.create(
				email='user@example.com', 
				amount=0,
				quality='normal',
			)
