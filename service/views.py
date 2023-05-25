from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import PurchaseForm
from .models import Purchase, Payment
from datetime import datetime, timedelta
from decimal import Decimal

def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            purchase = form.save(commit=False)
            purchase.credit_amount = purchase.purchase_price * Decimal(0.75)
            if purchase.credit_amount > 60000:
                purchase.credit_amount = 60000
            purchase.debt = purchase.credit_amount + purchase.credit_amount * purchase.commission / 100
            purchase.save()
            months = purchase.credit_term
            payment_amount = round(purchase.debt / months, 2)
            payment_date = purchase.created_at.date() + timedelta(days=30)
            for i in range(months):
                if i == months - 1:
                    if not purchase.commission_held:
                        payment_amount += purchase.commission
                        purchase.commission_held = True
                        purchase.save()
                Payment.objects.create(purchase=purchase, amount=payment_amount, due_date=payment_date)
                payment_date += timedelta(days=30)
            return HttpResponseRedirect(reverse('purchase_detail', args=[purchase.pk]))
    else:
        form = PurchaseForm()
    return render(request, 'purchases/purchase_form.html', {'form': form})

def purchase_detail(request, pk):
    purchase = Purchase.objects.get(pk=pk)
    payments = purchase.payment_set.all()
    return render(request, 'purchases/purchase_detail.html', {'purchase': purchase, 'payments': payments})

