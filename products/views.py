from django.shortcuts import render
from django.http import HttpResponse, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import * 
from cart.models import * 


from collections import defaultdict

import pandas as pd
import urllib.parse

# to serialize to json format 
from django.core import serializers

from django.core.mail import send_mail
from django.conf import settings

def index(request):
    if not request.session.session_key:
        ck_message = 'not'
        request.session.create()
        current_session_key = request.session.session_key
    else:
        ck_message = 'yes'
        current_session_key = request.session.session_key
    
    cart = Cart.objects.get_or_create(session_key = current_session_key)[0]

    br = Brand.objects.all()
    allcategories = Category.objects.all()

    products = Product.objects.all()

    popular_products = Product.objects.order_by('-product_rate')[:10]

    last_viewed = ViewedProduct.objects.filter(
        cart = cart
    ).values('pr_id')

    last_viewed_products = Product.objects.filter(id__in = last_viewed)


    return render(request, 'products/index.html', {
        'ck_message': ck_message,
        'allbrands': br,
        'categories': allcategories,

        'products': products,
        'popular_products': popular_products,
        'last_viewed_products': last_viewed_products,
    })

def brand(request, brand_id):
    if not request.session.session_key:
        ck_message = 'not'
        request.session.create()
        current_session_key = request.session.session_key
    else:
        ck_message = 'yes'
        current_session_key = request.session.session_key
    
    cart = Cart.objects.get_or_create(session_key = current_session_key)[0]

    allbrands = Brand.objects.all()
    allcategories = Category.objects.all()
    br = Brand.objects.get(id = brand_id)
    series = br.series_set.all()
    products = Product.objects.filter(pr_brand = br)
    return render(request, 'products/brand.html', {
        'allbrands': allbrands,
        'categories': allcategories,
        'products': products,
        'brand': br,
        'current_brand': br.id,
        'series': series,
    })

def series(request, brand_id, series_id):
    if not request.session.session_key:
        ck_message = 'not'
        request.session.create()
        current_session_key = request.session.session_key
    else:
        ck_message = 'yes'
        current_session_key = request.session.session_key
    
    cart = Cart.objects.get_or_create(session_key = current_session_key)[0]

    allbrands = Brand.objects.all()
    allcategories = Category.objects.all()

    br = Brand.objects.get(id = brand_id)
    ser = Series.objects.get(id = series_id)
    products = Product.objects.filter(pr_brand  = br, pr_series = ser)
    return render(request, 'products/series.html', {
        'allbrands': allbrands,
        'categories': allcategories,

        'products': products,
        'current_brand': br.id,
        'current_ser': ser.id,
        'series': ser,
    })

def category(request, category_id):
    if not request.session.session_key:
        ck_message = 'not'
        request.session.create()
        current_session_key = request.session.session_key
    else:
        ck_message = 'yes'
        current_session_key = request.session.session_key
    
    cart = Cart.objects.get_or_create(session_key = current_session_key)[0]

    br = Brand.objects.all()
    allcategories = Category.objects.all()
    current_category = category_id
    products = Product.objects.filter(pr_category__id = category_id)

    curr_br = products.values('pr_brand').distinct()
    print(curr_br)
    current_brands_filter = Brand.objects.filter(id__in = curr_br)

    return render(request, 'products/category.html', {
        'allbrands': br,
        'categories': allcategories,
        'current_category': current_category,
        'products': products,
        'current_brands_filter': current_brands_filter,
    })

def filter_products(request):
    br = Brand.objects.all()
    allcategories = Category.objects.all()

    products = Product.objects.all()
    f_hair = []
    f_prtype = []
    f_dest = []
    f_brands = []

    if (request.GET['brand']):
        brand = request.GET['brand']
        products = products.filter(pr_brand__id = brand)
    if (request.GET['series']):
        series = request.GET['series']
        products = products.filter(pr_series__id = series)
    if (request.GET['cat_id']):
        category = request.GET['cat_id']
        products = products.filter(pr_category__id = category)

    if (request.GET['brands_filter']):
        current_brands_filter = request.GET['brands_filter'].split(',')
        for item in current_brands_filter:
            f_brands.append(int(item))
    if (request.GET['hair_filters']):
        hair = request.GET['hair_filters'].split(',')
        for item in hair:
            f_hair.append(item)
    if (request.GET['prtype_filters']):
        prtype = request.GET['prtype_filters'].split(',')
        for item in prtype:
            f_prtype.append(item)
    if (request.GET['dest_filters']):
        dest = request.GET['dest_filters'].split(',')
        for item in dest:
            f_dest.append(item)


    if len(f_hair) > 0:
        products = products.filter(pr_hairtype__id__in = f_hair)
    if len(f_prtype) > 0: 
        products = products.filter(pr_prtype__id__in = f_prtype)
    if len(f_dest) > 0:
        products = products.filter(pr_destination__id__in = f_dest)
    if len(f_brands) > 0:
        
        products = products.filter(pr_brand__id__in = f_brands)

    
    pid = products.values('id').distinct()
    products = Product.objects.filter(id__in = pid)

    if len(products) < 1:
        return render(request, 'products/blocks/noprfilter.html', {
           'allbrands': br,
           'categories': allcategories, 
        })
    else:

        return render(request, 'products/blocks/pr_flist.html', {
            'allbrands': br,
            'categories': allcategories,

            'products': products,
        })


def product_page(request, product_id):
    if not request.session.session_key:
        ck_message = 'not'
        request.session.create()
        current_session_key = request.session.session_key
    else:
        ck_message = 'yes'
        current_session_key = request.session.session_key
    try:
        cart = Cart.objects.get_or_create(session_key = current_session_key)[0]
    except:
        pass


    allbrands = Brand.objects.all()
    allcategories = Category.objects.all()
    print('get product page request')
    current_product = Product.objects.get(id = product_id)
    current_product.product_rate += 1
    current_product.save()

    try:
        current_viewed = ViewedProduct(
            cart = cart,
            pr_id = current_product.id,
        )
        current_viewed.save()
    except:
        pass

    return render(request, 'products/product_page.html', {
        'allbrands': allbrands,
        'categories': allcategories,

        'product': current_product,
    })

def search(request):
    search_query = request.GET['q']
    allbrands = Brand.objects.all()
    allcategories = Category.objects.all()
    pr = Product.objects.all()
    search = search_query.split(" ")
    for item in search:
        pr = pr.filter(name__icontains = item)

    return render(request, 'products/search.html', {
        'allbrands': allbrands,
        'categories': allcategories,
        'products': pr,
        'search_query': search_query,
    })  

def search_ajax(request):
    pr = Product.objects.all()
    s = request.GET['q']
    s = s.split(",")
    for item in s:
        if len(item) > 0:
            # new_query = Product.objects.filter(name__icontains = item)
            pr = pr.filter(name__icontains = item)

    # if len(pr) > 1:
    return render(request, 'products/search_ajax.html', {
        'products': pr,
    })
    # else:
    #     return HttpResponse(status = 204)

def aboutus(request):
    allbrands = Brand.objects.all()
    allcategories = Category.objects.all()
    return render(request, 'products/about_us.html', {
        'allbrands': allbrands,
        'categories': allcategories,
    })

def delivery_info(request):
    allbrands = Brand.objects.all()
    allcategories = Category.objects.all()
    return render(request, 'products/delivery_info.html', {
        'allbrands': allbrands,
        'categories': allcategories,
    })
def payment_info(request):
    allbrands = Brand.objects.all()
    allcategories = Category.objects.all()
    return render(request, 'products/payment_info.html', {
        'allbrands': allbrands,
        'categories': allcategories,
    })
def partners_info(request):
    allbrands = Brand.objects.all()
    allcategories = Category.objects.all()
    return render(request, 'products/partners_info.html', {
        'allbrands': allbrands,
        'categories': allcategories,
    })
def take_back(request):
    allbrands = Brand.objects.all()
    allcategories = Category.objects.all()
    return render(request, 'products/take_back.html', {
        'allbrands': allbrands,
        'categories': allcategories,
    })
def contact_info(request):
    allbrands = Brand.objects.all()
    allcategories = Category.objects.all()
    return render(request, 'products/contact_info.html', {
        'allbrands': allbrands,
        'categories': allcategories,
    })

def contact_form_ajax(request): 
    name = request.GET['name']
    phone = request.GET['phone']
    print('name is', name)
    print('phone is', phone)

    send_mail(
    'Новая заявка на сайте!',
    'Имя: {} .Номер: {} '.format(name, phone),
    settings.EMAIL_HOST_USER,
    ['proff-butik@mail.ru'],
    )
    return JsonResponse({
        'success': 'true',
    }, status = 200)






