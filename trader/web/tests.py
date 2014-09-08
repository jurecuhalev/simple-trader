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
		pass

	def test_list_trades_is_displayed(self):
		order = TradeOrder.objects.create(
			email='user@example.com', 
			amount=10,
			quality='normal',
		)

		response = self.client.get('/')
		self.assertContains(response, order.email)

		order.delete()

	def test_api_not_working(self):
		pass

	def test_api_price_unavailable_handled(self, mock_requests):
		pass

	def test_api_price_available(self, mock_requests):
		pass

	def tearDown(self):
		pass

class OrderAddTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_that_form_is_displayed(self):
		pass

	def test_that_correct_form_is_used(self):
		from web.forms import OrderAddForm
		
		response = self.client.get('/add/')
		self.assertIsInstance(response.context['form'], OrderAddForm)

	def test_form_add(self):
		pass

	def test_form_with_gmail_fails(self):
		pass

	def test_form_with_zero_amount(self):
		pass

	def test_homepage_do_not_list_expired_order(self):
		pass

class OrderDetailTest(TestCase):
	def setUp(self):
		self.client = Client()

	def test_display_order(self):
		pass

	def test_do_not_display_expired_order(self):
		pass

class TradeOrderModelTest(TestCase):

	def test_require_one_or_more_order_amount(self):
		pass
