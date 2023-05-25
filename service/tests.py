
from django.test import TestCase, Client
from django.urls import reverse
from .models import Purchase, Payment


class PurchaseCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.form_data = {
            'full_name': 'Иван Сидоров',
            'phone_number': '+79999999999',
            'purchase_price': 50000,
            'credit_term': 4,
            'commission': 5
        }

    def test_purchase_create_post_valid_form(self):
        response = self.client.post(reverse('purchase_create'), self.form_data)
        self.assertEqual(response.status_code, 302)
        purchase = Purchase.objects.get(full_name=self.form_data['full_name'])
        self.assertRedirects(response, reverse('purchase_detail', args=[purchase.pk]))
        self.assertEqual(purchase.purchase_price, self.form_data['purchase_price'])
        self.assertEqual(purchase.credit_amount, 37500)
        self.assertEqual(purchase.debt, 39375)
        self.assertEqual(purchase.commission_held, False)
        payments = Payment.objects.filter(purchase=purchase)
        self.assertEqual(len(payments), 4)
        self.assertEqual(payments[0].amount, 9843.75)