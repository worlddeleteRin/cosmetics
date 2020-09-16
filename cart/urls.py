
from django.urls import path, include
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_item/<str:product_id>', views.add_item, name = 'add_item'),
    path('remove_item_ajax/', views.remove_item_ajax, name = 'remove_item_ajax'),
    path('add_item_ajax/', views.add_item_ajax, name = 'add_item_ajax'),
    path('update_item_amount_ajax/', views.update_item_amount_ajax, name = 'update_item_amount_ajax'),
    path('update_total_amount_ajax/', views.update_total_amount_ajax, name = 'update_total_amount_ajax'),
    path('remove_item_from_cart_ajax/', views.remove_item_from_cart_ajax, name = 'remove_item_from_cart_ajax'),
    path('add_to_cart_ajax/', views.add_to_cart_ajax, name = 'add_to_cart_ajax'),
    path('create_order_ajax/', views.create_order_ajax, name = 'create_order_ajax'),
    path('add_quantity/<str:item_id>', views.add_quantity, name = 'add_quantity'),
    path('remove_quantity/<str:item_id>', views.remove_quantity, name = 'remove_quantity'),
    path('update_nav_total/', views.update_nav_total, name = 'update_nav_total'),
    path('check_promo_ajax/', views.check_promo_ajax, name = 'check_promo_ajax'),
    path('set_promo/', views.set_promo, name = 'set_promo'),
]
