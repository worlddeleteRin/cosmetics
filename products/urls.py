
from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index, name='index'),
    path('brand/<str:brand_id>', views.brand, name = 'brand'),
    path('brand/<str:brand_id>/<str:series_id>', views.series, name = 'series'),
    path('category/<str:category_id>', views.category, name = 'category'),
    path('filter_products/', views.filter_products, name = 'filter_products'),
    path('product/<str:product_id>', views.product_page, name='product_page'),
    path('search/', views.search, name='search'),
    path('search_ajax/', views.search_ajax, name='search_ajax'),

    path('contact_form_ajax', views.contact_form_ajax, name="contact_form_ajax"),
    path('about_us', views.aboutus, name = 'aboutus'),
    path('delivery_info', views.delivery_info, name = 'delivery_info'),
    path('payment_info', views.payment_info, name = 'payment_info'),
    path('partners_info', views.partners_info, name = 'partners_info'),
    path('contact_info', views.contact_info, name = 'contact_info'),
    path('take_back', views.take_back, name = 'take_back'),
]
