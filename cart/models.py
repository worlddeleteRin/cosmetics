from django.db import models

# Create your models here.


class Promocode(models.Model):
    name = models.CharField(max_length = 200, default = '')
    discount = models.IntegerField(default = 0)
    

class Cart(models.Model):  
    created_at = models.DateTimeField(auto_now_add = True) 
    session_key = models.CharField(max_length = 200)

    promo = models.ForeignKey(
        Promocode, on_delete = models.DO_NOTHING, default = None,
    blank = True, null = True
    )

    def get_total(self):
        total = 0
        for item in self.item_set.all():
            total += item.price * item.quantity
        return total
    def if_items_empty(self):
        if (len(self.item_set.all()) < 1):
            return True
        else:
            return False
    def get_total_promo(self):
        total = 0
        for item in self.item_set.all():
            total += item.price * item.quantity
        if (self.promo != None):
            total = total - ((total * self.promo.discount) / 100)
        return total

class ViewedProduct(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete = models.CASCADE, default = None,
        blank = True, null = True
    )
    pr_id = models.IntegerField()

class Orders(models.Model):

    name = models.CharField(max_length = 200, default = '')
    phone = models.CharField(max_length = 50, default = '')
    email = models.CharField(max_length = 200, default = '')

    delivery = models.CharField(max_length = 200, default = '')
    payment = models.CharField(max_length = 200, default = '')
    city = models.CharField(max_length = 70, default = '')
    # index_code = models.CharField(max_length = 20, default = '')
    address = models.CharField(max_length = 400, default = '')
    order_price = models.IntegerField(max_length = 10, default = 0)
    comment = models.CharField(max_length = 3000, default = '')



class Item(models.Model):
    cart = models.ForeignKey(Cart, on_delete = models.CASCADE, default = None,
    blank = True, null = True)
    order = models.ForeignKey(Orders, on_delete = models.CASCADE, 
    default = None, blank = True, null = True )

    name = models.CharField(max_length = 200, default = '')
    price = models.IntegerField(default = 0)
    imgurl = models.CharField(max_length = 300, default = '')
    quantity = models.IntegerField(default = 1)

    def product_order_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.name 
    

def delete_all_cart():
    carts = Cart.objects.all()
    items = Item.objects.all()
    orders = Orders.objects.all()
    carts.delete()
    print("All carts are deleted")
    items.delete()
    print("All items are deleted")
    orders.delete()
    print("All orders are deleted")





