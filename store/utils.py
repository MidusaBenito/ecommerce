import json
from . models import *
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('cart:', cart)
    items = []
    order = {'get_cart_total':0 ,'get_cart_items': 0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        j = i.split(',')
        print(j)
        try:
            cartItems += cart[i]['quantity']
            sandle = Sandle.objects.get(id=j[0])
            size = Size.objects.get(id=j[1])
            total = (sandle.price * cart[i]['quantity'])
            order['get_cart_total'] += total 
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                    'id':sandle.id,
                  'sandle': {
                     'id':sandle.id,
                     'name':sandle.name,
                     'price':sandle.price,
                     'image':sandle.image
                    },
                    'size':{
                        'id':size.id, 
                        'size':size.size,
                    },
                    'quantity':cart[i]['quantity'],
                    'get_total':total,
                    }
            items.append(item)
            if sandle.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'cartItems':cartItems, 'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems, 'order':order, 'items':items}

def guestOrder(request, data):
    print('User is not logged in...')
    print('COOKIES:', request.COOKIES)
    first_name = data['form']['first_name']
    last_name = data['form']['last_name']
    email = data['form']['email']
    phone = data['form']['phone']

    cookieData = cookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
            email=email,
        )
    customer.first_name = first_name
    customer.last_name = last_name
    customer.phone = phone
    customer.save()

    order = Order.objects.create(
            customer=customer,
            complete=False,
        )
    for item in items:
        sandle = Sandle.objects.get(id=item['sandle']['id'])
        orderItem = OrderItem.objects.create(
                sandle=sandle,
                order=order,
                quantity=item['quantity']
            )
    return customer, order

def get_sandles(request):
    sandles = Sandle.objects.all()
    return sandles

"""def sizes(request):
    all_sandles = get_sandles(request)
    for sandle in all_sandles:  
        cat = (sandle.category)
        sizes = Category.objects.get(name=cat).sizes.order_by('-id')[:8]
        return sizes """

def men_sandles(request):
    sizes = Category.objects.get(id=1).sizes.order_by('-id')
    return sizes

def ladies_sandles(request):
    sizes = Category.objects.get(id=2).sizes.order_by('-id')
    return sizes

def kids_sandles(request):
    sizes = Category.objects.get(id=3).sizes.order_by('-id')
    return sizes


