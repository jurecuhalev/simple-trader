from django.test import TestCase
from django.test.client import Client

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
			quality='normal',
		)

		response = self.client.get('/')
		self.assertContains(response, order.email)

		order.delete()

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

	def test_do_not_display_expired_trade(self):
		pass

