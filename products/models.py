from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length = 100, default = '')
    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length = 100, default = '')
    def __str__(self):
        return self.name

class Prtype(models.Model):
    name = models.CharField(max_length = 100, default = '')
    def __str__(self):
        return self.name

class Hairtype(models.Model):
    name = models.CharField(max_length = 100, default = '')
    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length = 100, default = '')
    description = models.CharField(max_length = 2000, default = '')
    # imgurl = models.CharField(max_length = 1000, default = '')
    imgurl = models.ImageField(upload_to='static/images', blank = True, null = True)
    def __str__(self):
        return self.name

class Series(models.Model):
    ser_brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)

    name = models.CharField(max_length = 100, default = '')
    description = models.CharField(max_length = 2000, default = '')
    imgurl = models.CharField(max_length = 1000, default = 'https://placehold.it/300x300')
    def __str__(self):
        return self.name

class Product(models.Model):
    pr_brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING)

    pr_series = models.ManyToManyField(Series)
    pr_prtype = models.ManyToManyField(Prtype)
    pr_category = models.ManyToManyField(Category)
    pr_destination = models.ManyToManyField(Destination)
    pr_hairtype = models.ManyToManyField(Hairtype)

    name = models.CharField(max_length=200, default = '')
    price = models.IntegerField()
    description = models.CharField(max_length = 2000, default = '')
    obiem = models.CharField(max_length = 10, default = '')
    # imgurl = models.CharField(max_length = 2000, default = '')
    imgurl = models.ImageField(upload_to='static/images/products', blank = True, null = True)    
    product_rate = models.IntegerField(default = 0)

    def __str__(self):
        return self.name


def deleteall():
    cat = Category.objects.all()
    dest = Destination.objects.all()
    prtype = Prtype.objects.all()
    hair = Hairtype.objects.all()
    brand = Brand.objects.all()
    ser = Series.objects.all()
    pr = Product.objects.all()


    pr.delete()
    ser.delete()
    brand.delete()
    cat.delete()
    dest.delete()
    prtype.delete()
    hair.delete()
    
    print("Everything is deleted")





