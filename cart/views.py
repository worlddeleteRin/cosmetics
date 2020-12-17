from django.shortcuts import render
from django.http import HttpResponse, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import * 
from products.models import * 

from collections import defaultdict

import pandas as pd
import urllib.parse

# to serialize to json format 
from django.core import serializers

from django.core.mail import send_mail
from django.conf import settings

from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

def index(request):
    allcategories = Category.objects.all()
    allbrands = Brand.objects.all()

    if not request.session.session_key:
        request.session.create()
        current_session_key = request.session.session_key
    else:
        current_session_key = request.session.session_key
    
    cart = Cart.objects.get_or_create(
        session_key = current_session_key
    )
    cart_items = cart[0].item_set.all()

    return render(request, 'cart/index.html', {
        'allbrands': allbrands,
        'categories': allcategories,
        'session_key': current_session_key,
        'items': cart_items,
        'current_cart': cart[0],
    })

def add_item(request, product_id):
    product = Product.objects.get(id = product_id)

    if not request.session.session_key:
        request.session.create()
        current_session_key = request.session.session_key
    else:
        current_session_key = request.session.session_key
    
    cart = Cart.objects.get_or_create(session_key = current_session_key)[0]
    cart_items = cart.item_set.all()
    if Item.objects.filter(cart = cart, name = product.name).exists():
        current_item = Item.objects.get(cart = cart, name = product.name)
        current_item.quantity += 1
        current_item.save()
    else:
        new_item = Item(
            cart = cart,
            name = product.name,
            price = product.price,
            sale_price = product.sale_price,
            imgurl = product.imgurl,
            brand = product.pr_brand.name,
            series = product.pr_series.name,
            obiem = product.obiem,
        )
        new_item.save()
    return HttpResponseRedirect(reverse('cart:index'))

def add_quantity(request, item_id):
    
    
    current_item = Item.objects.get(id = item_id)
    current_item.quantity += 1
    current_item.save()
    return HttpResponseRedirect(reverse('cart:index'))

def remove_quantity(request, item_id):
    current_session_key = request.session.session_key
    cart = Cart.objects.get_or_create(session_key = current_session_key)[0]
    current_item = Item.objects.get(id = item_id)
    if current_item.quantity == 1:
        current_item.delete()
    else:
        current_item.quantity -= 1
        current_item.save()
    return HttpResponseRedirect(reverse('cart:index'))

def remove_item_ajax(request):
    current_session_key = request.session.session_key
    cart = Cart.objects.get(session_key = current_session_key)
    item_id = request.GET['item_id']
    current_item = Item.objects.get(id = item_id, cart = cart)
    if current_item.quantity == 1:
        current_item.delete()
        return JsonResponse({
        'message': 'everything is ok',
        'need_delete': 'yes',
        }, status = 200)
        check_items = cart.if_items_empty()
        if check_items == True:
            cart.promo = None
            cart.save()
    else:
        current_item.quantity -= 1
        current_item.save()
        quantity = current_item.quantity
        return JsonResponse({
            'message': 'everything is ok',
            'need_delete': 'no',
            'quantity': quantity,
        }, status = 200)


def add_item_ajax(request):
    if not request.session.session_key:
        request.session.create()
        current_session_key = request.session.session_key
    else:
        current_session_key = request.session.session_key
    cart = Cart.objects.get_or_create(session_key = current_session_key)[0]
    item_id = request.GET['item_id']
    current_item = Item.objects.get(id = item_id, cart = cart)
    current_item.quantity += 1
    current_item.save()
    quantity = current_item.quantity
    return JsonResponse({
        'message': 'everything is ok',
        'quantity': quantity,
    }, status = 200)

def update_item_amount_ajax(request):
    current_session_key = request.session.session_key
    cart = Cart.objects.get(session_key = current_session_key)
    item_id = request.GET['item_id']
    current_item = Item.objects.get(id = item_id, cart = cart)
    if current_item.sale_price:
        amount = current_item.quantity * current_item.sale_price
    else:
        amount = current_item.quantity * current_item.price
    return JsonResponse({
        'message': 'everything is ok',
        'item_amount': amount,
    }, status = 200)

def update_total_amount_ajax(request):

    current_session_key = request.session.session_key
    cart = Cart.objects.get(session_key = current_session_key)
    total_amount = cart.get_total()

    if cart.promo != None:
        total_amount_promo = cart.get_total_promo()
        has_promo = 'true'
        return JsonResponse({
            'total_amount_promo': total_amount_promo,
            'message': 'everything is ok',
            'total_amount': total_amount,
            'has_promo': has_promo,
        }, status = 200)
    else:
        has_promo = 'false'
        return JsonResponse({
            'message': 'everything is ok',
            'total_amount': total_amount,
            'has_promo': has_promo,
        }, status = 200)


def remove_item_from_cart_ajax(request):
    current_session_key = request.session.session_key
    cart = Cart.objects.get(session_key = current_session_key)
    current_item_id = request.GET['item_id']
    print('item id is',current_item_id )
    current_item = Item.objects.get(cart = cart, id = current_item_id)
    print(current_item)
    current_item.delete()

    check_items = cart.if_items_empty()
    if check_items == True:
            cart.promo = None
            cart.save()

    return JsonResponse({
        'message': 'everything is ok',
    }, status = 200)

def add_to_cart_ajax(request):

    if not request.session.session_key:
        request.session.create()
        current_session_key = request.session.session_key
    else:
        current_session_key = request.session.session_key
    cart = Cart.objects.get_or_create(session_key = current_session_key)[0]
    current_product_id = request.GET['product_id']
    
    current_product = Product.objects.get(id = current_product_id)
    message = ""

    if Item.objects.filter(cart = cart, name = current_product.name,
    price = current_product.price).exists():
        item = Item.objects.get(cart = cart, name = current_product.name,
        price = current_product.price)
        item.quantity += 1
        item.save()
    else:
        item = Item(
            cart = cart, 
            name = current_product.name,
            price = current_product.price,
            sale_price = current_product.sale_price,
            imgurl = current_product.imgurl,
            brand = current_product.pr_brand.name,
            series = current_product.pr_series.name,
            obiem = current_product.obiem,
        )
        item.save()


    return JsonResponse({
        'message': 'Товар добавлен в корзину!',
    }, status = 200)

def create_order_ajax(request):
    current_session_key = request.session.session_key
    cart = Cart.objects.get(session_key = current_session_key)
    cart_items = cart.item_set.all()

    # parse cart info 
    delivery_method = request.GET['delivery_method']
    delivery_method = urllib.parse.unquote(delivery_method)
    delivery_cost = request.GET['delivery_cost']
    payment_method = request.GET['payment_method']
    payment_method = urllib.parse.unquote(payment_method)
    customer_name = request.GET['customer_name']
    customer_name = urllib.parse.unquote(customer_name)
    customer_phone = request.GET['customer_phone']
    customer_city = request.GET['customer_city']
    customer_city = urllib.parse.unquote(customer_city)
    customer_address = request.GET['customer_address']
    customer_address = urllib.parse.unquote(customer_address)
    order_comment = request.GET['cart_comment']
    order_comment = urllib.parse.unquote(order_comment)
    customer_email = request.GET['customer_email']
    customer_email = urllib.parse.unquote(customer_email)

    order_price = int(delivery_cost) + cart.get_total_promo()

    new_order = Orders(
        name = customer_name,
        phone = customer_phone,
        email = customer_email,
        delivery = delivery_method + ' ' + delivery_cost,
        payment = payment_method,
        city = customer_city,
        address = customer_address,
        order_price = order_price,
        comment = order_comment,
    )
    new_order.save()

    cart_items_mail = []
    order_price_mail = order_price
    order_comment_mail = order_comment
    customer_address_mail = customer_city + ', ' +  customer_address
    delivery_method_mail = delivery_method
    order_id = new_order.id

    for item in cart_items:
        new_order.item_set.add(item)
        cart_items_mail.append([item.name, item.quantity, item.price])

    for item in cart.item_set.all():
        cart.item_set.remove(item)

    cart.promo = None
    cart.save()

    cart_items_all = new_order.item_set.all()

    context = {
        'order_id': order_id,
        'order_price_mail': order_price_mail,
        'name': customer_name,
        'phone': customer_phone,
        'email': customer_email,
        'delivery_address': customer_address_mail,
        'cart_items_all': cart_items_all,
        'delivery_method_mail': delivery_method_mail,
        'order_comment_mail': order_comment_mail,
    }
    client_html_message = render_to_string('cart/blocks/order_mail_template.html', context)
    client_html_message_plain = strip_tags(client_html_message)

    admin_html_message = render_to_string('cart/blocks/order_mail_template_admin.html', context)
    admin_html_message_plain = strip_tags(admin_html_message)

    try:
        send_mail(
        'Заказ № {}'.format(order_id),
        admin_html_message_plain,
        settings.EMAIL_HOST_USER,
        [
            'worlddelete0@mail.ru',
            'proff-butik@mail.ru'
        ],
        html_message = admin_html_message
        )
        print('mail is sent')

        print('try to send mail')
        send_mail(
        'Заказ № {}'.format(order_id),
        client_html_message_plain,
        settings.EMAIL_HOST_USER,
        [
            customer_email,
            # 'proff-butik@mail.ru'
        ],
        html_message = client_html_message
        )
    except: 
        print('was an error when send mail')

    return JsonResponse({
        'order_created': 'yes',
    }, status = 200)


def update_nav_total(request):

    if not request.session.session_key:
        request.session.create()
        current_session_key = request.session.session_key
    else:
        current_session_key = request.session.session_key
    cart = Cart.objects.get_or_create(session_key = current_session_key)[0]
    cart_total = cart.get_total()
    return JsonResponse({
        'cart_total': cart_total,
    }, status = 200)

def check_promo_ajax(request):
    current_session_key = request.session.session_key
    cart = Cart.objects.get(session_key = current_session_key)


    current_promo = request.GET['promo']
    if Promocode.objects.filter(name = current_promo).exists():
        print('this promo exist')
        promo = Promocode.objects.get(name = current_promo)
        cart.promo = promo
        cart.save()

        return JsonResponse({
            'exist': 'yes',
        }, status = 200)
    else:
        print('this promo not exist')
        return JsonResponse({
            'exist': 'no',
        }, status = 200)

def set_promo(request):
    current_session_key = request.session.session_key
    cart = Cart.objects.get(session_key = current_session_key)

    if cart.promo != None:
        print('promo exist')
        promo_name = cart.promo.name
        return JsonResponse({
            'promo_name': promo_name,
            'exist': 'yes'
        }, status = 200)
    else:
        return JsonResponse({
            'exist': 'no'
        }, status = 200)

        



    

