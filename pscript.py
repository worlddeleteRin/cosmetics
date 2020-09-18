#!/usr/bin/env python3

from products.models import *
import pandas as pd
import numpy as np
from os import walk
import pandas as pd
import requests
import base64


def create_categories():
    print('------------------')
    print('start creating categories')
    print('------------------')
    cat = [
        'уход',
        'стайлинг',
        'кератин и ботокс',
    ]
    for item in cat:
        new_cat = Category(
            name = item
        )
        new_cat.save()

def make_products_file():
    print('------------------')
    print('start making products file')
    print('------------------')
    path_files = '/Users/noname/work/inna/goods/xl/'
    export_path = '/Users/noname/work/inna/goods/new/'
    data_tmp = []
    for (dirname, dirpath, filename) in walk(path_files):
        for file in filename:
            if 'xlsx' in file:
                tmp = pd.read_excel(path_files + file)
                data_tmp.append(tmp)
        data = pd.concat(data_tmp, ignore_index=True)
    
    data = data.replace('Для всех типов', 'Все типы')
    data = data.replace('для всех типов', 'Все типы')
    data = data.replace('все типы', 'Все типы')

    data["nazhnachenie"] = data["nazhnachenie"].str.split("|")
    data["tip_volos"] = data["tip_volos"].str.split("|")
    data["product_type"] = data["product_type"].str.split("|")
    data["category"] = data["category"].str.split("|")
    data["lineika"] = data["lineika"].str.split("|")
    data.to_csv(export_path + 'data.csv')
    print('data file created, shape is: ', data.shape)

def make_products_final():
    print('------------------')
    print('start making products final')
    print('------------------')
    products_path = '/Users/noname/work/inna/goods/new/data.csv'
    to_save = '/Users/noname/work/inna/cosmetics/static/images/products/'
    export_path = '/Users/noname/work/inna/goods/new/'
    data = pd.read_csv(products_path)
    for index, item in data.iterrows():
        # pass
        current_url = item["imgurl"]
        print('downloading image:', current_url)
        if str(current_url) != 'nan':
            if 'data:image' in current_url:
                header, encoded = current_url.split(',', 1)
                image_format = header.split('/', 1)[1].split(';')[0]
                dec = base64.b64decode(encoded)
                image_name = 'product_image_' + str(index) + '.' + image_format
                file = open(to_save + image_name , "wb")
                file.write(dec)
                file.close()
                data['imgurl'][index] = image_name
            else:
                r = requests.get(current_url, verify = False)
                if r.status_code == 200:
                    image_format = r.headers['Content-Type'].split('/')[1]
                    image_name = 'product_image_' + str(index) + '.' + image_format
                    file = open(to_save + image_name , "wb")
                    file.write(r.content)
                    file.close()
                    data['imgurl'][index] = image_name
                else:
                    print('продукт по id', index, ' не может скачать изображение')
        else:
            print('no image specified')
        data.to_csv(export_path + 'data2.csv')



def make_series_file():
    print('------------------')
    print('make series file')
    print('------------------')
    ser_path = '/Users/noname/work/inna/goods/series/series_template4.xlsx'
    export_path = '/Users/noname/work/inna/goods/new/series.csv'
    data = pd.read_excel(ser_path)
    data.to_csv(export_path)


def createseries(series_data):
    print('------------------')
    print('start creating series')
    print('------------------')
    i = 0
    for index, item in series_data.iterrows():
        brand_name = item['brand'].lower()
        if (Brand.objects.filter(name = brand_name).exists()):
            brand = Brand.objects.get(name = brand_name)
            name = item['name'].strip()
            # name = name.lower()
            new_ser = Series(
                ser_brand = brand,
                name = name,
                description = item['description'],
                imgurl = item['imgurl'],
            )
            new_ser.save()
            print('created series:', item['name'])
        else:
            print('series: ', item['name'] )
            print('Not found brand:', brand_name)
        


def createbrands(brands_data):
    print('------------------')
    print('start creating brands')
    print('------------------')
    i = 0
    for index, item in brands_data.iterrows():
        brand_name = item['name'].lower()
        brand_description = item['description']
        brand_image = item['imgurl']
        new_brand = Brand.objects.get_or_create(
            name = brand_name,
            description = brand_description,
            imgurl = brand_image,
        )
        i = i + 1
    print('created', i, 'brands')


def createproducts(products_data, series_not_created):
    print('------------------------')
    print('start creating products')
    print('------------------------')
    i = 0
    rows = 0
    nf_series = 0
    not_ser = []
    for index, item in products_data.iterrows(): 
        
        rows = rows + 1
        brand_name = item["proizvoditel"].lower()
        current_brand = Brand.objects.get_or_create(name=brand_name)[0]
        # curr_ser = item["lineika"]
        # if Series.objects.filter(name__iexact = curr_ser).exists():
        #     current_series = Series.objects.get(
        #         name__iexact = curr_ser,
        #         ser_brand = current_brand,
        #     )

        price = item["price"].replace(" ", "")
        price = int(price)
        new_product = Product(
        pr_brand = current_brand,
        # pr_series = current_series,
        name = item["name"],
        price = price,
        description = item["description"],
        obiem = item["obiem"],
        imgurl = item["imgurl"],
    )
        new_product.save()
            
        if type(item["nazhnachenie"])  == str:
            for n in eval(item["nazhnachenie"]):
                n = n.strip()
                destination = Destination.objects.get_or_create(name = n)[0]
                new_product.pr_destination.add(destination)
        if type(item["tip_volos"]) == str:
            for n in eval(item["tip_volos"]):
                n = n.strip()
                if n != '-':
                    hairtype = Hairtype.objects.get_or_create(name = n)[0]
                    new_product.pr_hairtype.add(hairtype)
        if type(item["category"]) == str:
            for n in eval(item["category"]):
                cname = n.lower()
                cname = cname.strip()
                print(cname)
                current_category = Category.objects.get_or_create(name = cname)[0]
                new_product.pr_category.add(current_category)
        if type(item["product_type"]) == str:
            for n in eval(item["product_type"]):
                n = n.strip()
                product_type = Prtype.objects.get_or_create(name = n)[0]
                new_product.pr_prtype.add(product_type)
        if type(item['lineika']) == str:
            for n in eval(item['lineika']):
                n = n.strip()
                # n = n.lower()
                if Series.objects.filter(name = n).exists():
                    current_series = Series.objects.get(name = n)
                    new_product.pr_series.add(current_series)
                else:
                    not_ser.append(np.array([item["name"], item["proizvoditel"], n]))
                    print('not found series:', n)
                    nf_series += 1
#         
        i = i + 1
        print('id: ', index, new_product.id, new_product.name, ' created')

        
    not_ser = np.asarray(not_ser)
    notser = pd.DataFrame(not_ser, columns=['name', 'brand', 'series'])
    notser.to_excel(series_not_created)
        
    print(rows,' processed')
    print('Created', i, 'products')
    print('Not found series: ', nf_series)
    
    
def createall():
    print('------------------')
    print('start creating all')
    print('------------------')
    products_data = pd.read_csv('/Users/noname/work/inna/goods/new/data2.csv')
    brands_data = pd.read_csv('/Users/noname/work/inna/goods/brands.csv')
    series_data = pd.read_csv('/Users/noname/work/inna/goods/new/series.csv')
    series_not_created = '/Users/noname/work/inna/goods/series/notser.xlsx'

    create_categories()
    createbrands(brands_data)
    createseries(series_data)
    createproducts(products_data, series_not_created)

if __name__ == '__main__':
    # make_products_file()
    # make_products_final()
    # make_series_file()
    createall()


    