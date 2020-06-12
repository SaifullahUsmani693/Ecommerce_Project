from django.shortcuts import render

# Create your views here.
from .models import *
from django.http import JsonResponse
import json
import datetime

# funcion del cart
from store.utils import cookieCart, cartData, guestOrder
# Filters
from .filters import Name_And_Price_Filter


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    tags = Tag.objects.all()
    brands = Brand.objects.all()
    Filters = Name_And_Price_Filter(request.GET, queryset=products)
    products = Filters.qs

    context = {'products': products, 'tags': tags,
               'cartItems': cartItems, 'Filters': Filters}
    return render(request, "store/store.html", context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, "store/checkout.html", context)


def updateItem(request):
    # Information Of What User Has Done
    data = json.loads(request.body.decode('utf-8'))
    # json.loads(request.body)
    # Product To Buy ID
    productID = data['productId']
    # Action To Add To Cart Or Something Else You Do
    action = data['action']
    # Print To Make Sure It Workds
    print('Action:', action)
    # Print To Make Sure It Workds
    print('productID:', productID)
    customer = request.user.customer
    product = Product.objects.get(id=productID)
    # create the order
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    #add or delete
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    # Show The Data Above Is Chrome Console As Well
    return JsonResponse('item was added', safe=False)


def processOrder(request):
    # print("Data",request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body.decode('utf-8'))
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
    return JsonResponse('Payment submitted..', safe=False)
