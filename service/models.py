from django.db import models
from datetime import datetime


class Purchase(models.Model):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2)
    credit_amount = models.DecimalField(max_digits=8, decimal_places=2)
    credit_term = models.IntegerField(choices=((4, '4 месяца'), (6, '6 месяцев')))
    commission = models.DecimalField(max_digits=8, decimal_places=2)
    commission_held = models.BooleanField(default=False)
    debt = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    class Payment(models.Model):
        purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
        amount = models.DecimalField(decimal_places=2, max_digits=10)
        due_date = models.DateField(default=datetime.now)
