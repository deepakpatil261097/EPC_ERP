from django.shortcuts import render
from .models import StockTransaction


def stock_summary(request):
    transactions = StockTransaction.objects.all()

    context = {
        'transactions': transactions
    }

    return render(request, 'inventory/stock_summary.html', context)