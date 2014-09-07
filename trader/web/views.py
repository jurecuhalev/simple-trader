import json
import random

import requests

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from web.models import TradeOrder
from web.forms import OrderAddForm

def index(request):
    active_order_lisit = TradeOrder.objects.all() #bug

    try:
        remote_api = requests.get('http://localhost:8000/price_api/')
    except requests.exceptions.ProtocolError:
        remote_api = None
    
    if remote_api and remote_api.status_code == 200:
        remote_data = json.loads(remote_api.content)
        current_price = remote_data.get('price')
    else:
        current_price = 'Unavailable'

    return render(request, 'web/index.html', {
        'active_order_lisit': active_order_lisit,
        'current_price': current_price
    })

def order_add(request):
    if request.method == 'POST':
        form = OrderAddForm(request.POST)
        if form.is_valid():
            order = TradeOrder.objects.create(
                email = form.cleaned_data.get('email'),
                amount = form.cleaned_data.get('amount'),
                quality = form.cleaned_data.get('quality')
            )
            
            return redirect(order.get_absolute_url())
    else:
        form = OrderAddForm()

    return render(request, 'web/order_add.html', {
        'form': form
    })

def order_view(request, order_id):
    order = get_object_or_404(TradeOrder, id=order_id)

    return render(request, 'web/order_detail.html', {
        'order': order
    })

def api_price(request):
    data = {'price': random.randint(1, 200)}    
    
    if random.randint(0, 10) > 8:
        return HttpResponseForbidden()

    return HttpResponse(json.dumps(data),
        mimetype='application/json')