from django import template

from products.models import * 

register = template.Library()

@register.simple_tag
def filter_hairtype(products): 
    htype = []
    for item in products:
        for it in item.pr_hairtype.all():
            htype.append(it.name)
    d = dict.fromkeys(htype)
    tlist = list(d)
    result = Hairtype.objects.filter(name__in = tlist)
    result = result.order_by("name")
    return result

@register.simple_tag
def filter_prtype(products): 
    ptype = []
    for item in products:
        for it in item.pr_prtype.all():
            ptype.append(it.name)
    d = dict.fromkeys(ptype)
    tlist = list(d)
    result = Prtype.objects.filter(name__in = tlist)
    result = result.order_by("name")
    return result


@register.simple_tag
def filter_destination(products): 
    pdest = []
    for item in products:
        for it in item.pr_destination.all():
            pdest.append(it.name)
    d = dict.fromkeys(pdest)
    tlist = list(d)
    result = Destination.objects.filter(name__in = tlist)
    result = result.order_by("name")
    return result

@register.simple_tag
def filter_series(products):
    pseries = []
    for item in products:
        for ser in item.pr_series.all():
            pseries.append(ser.id)
    d = dict.fromkeys(pseries)
    tlist = list(d)
    result = Series.objects.filter(
        id__in = tlist
    ) 
    result = result.order_by("name")
    return result

# @register.simple_tag
# def filter_obiem(products): 
#     pdest = []
#     for item in products:
#         pdest.append(item.obiem)
#     d = dict.fromkeys(pdest)
#     tlist = list(d)
#     # result = Destination.objects.filter(name__in = tlist)
#     # result = result.order_by("name")
#     result = tlist
#     return result

@register.simple_tag
def format_price(price):
    new_price = '{:,}'.format(price)
    return new_price


@register.simple_tag
def check_empty_query(qs):
    length = len(qs.all())
    return length

@register.simple_tag
def corrent_imgurl(imgurl):
    if ('/' in imgurl.name):
        corrent_url = imgurl.name.split('/')[-1]
        return corrent_url
    else:
        return imgurl
