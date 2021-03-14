from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from . utils import cookieCart, cartData, guestOrder, get_sandles, men_sandles, ladies_sandles, kids_sandles
from datetime import datetime, timedelta
from .forms import LoginForm, UserRegistrationForm, EditProfile
from django.contrib.auth.decorators import login_required 

# Create your views here.
def store(request, category_slug=None):
    category=None
    #data = cartData(request)
    #cartItems = data['cartItems']
    
    sandles = get_sandles(request)
    #sandle_sizes = sizes(request)
    men = Category.objects.get(id=1).products.order_by('-created')
    ladies = Category.objects.get(id=2).products.order_by('-created')
    children = Category.objects.get(id=3).products.order_by('-created')
    men_sizes = men_sandles(request)
    ladies_sizes = ladies_sandles(request)
    kids_sizes = kids_sandles(request)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        sandles = sandles.filter(category=category)
        #sandle_sizes = sandle_sizes.filter(category=category)
        #print(sandle_sizes)
    context = {"category": category,'sandles':sandles, "men":men, "ladies":ladies, "children":children, "men_sizes":men_sizes, "ladies_sizes":ladies_sizes, "kids_sizes":kids_sizes}
    return render(request, 'store/store.html', context) 

#def sandle_sizes(request):

def sandle_detail(request, id, slug):
    #data = cartData(request)
    #men_sizes=Category.objects.get(id=1).sizes.all()
    #ladies_sizes=Category.objects.get(id=2).sizes.all()
    #kids_sizes=Category.objects.get(id=3).sizes.all()
    #cartItems = data['cartItems']
    sandle = get_object_or_404(Sandle, id=id, slug=slug)
    cat = (sandle.category)
    sizes = Category.objects.get(name=cat).sizes.order_by('-id')
    due_date = datetime.now() + timedelta(days=7)
    due_date_2 = datetime.now() + timedelta(days=10)
    context_bound = {"sandle":sandle,"due_date":due_date, "due_date_2":due_date_2, "cat": cat, "sizes": sizes}
    return render(request, 
                    'store/detail.html', context_bound)

def cart(request):
    #data = cartData(request)
    #cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context) 

def checkout(request):
    #data = cartData(request)
    #cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', context) 

def updateItems(request):
    data = json.loads(request.body)
    sandleId = data['sandleId']
    sizeId = data['sizeId']
    action = data['action']
    print('Action:', action)
    print('Sandle:',sandleId)

    customer = request.user.customer
    sandle = Sandle.objects.get(id=sandleId)
    size = Size.objects.get(id=sizeId)
    order,created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, sandle=sandle, size=size)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
    else:
        customer, order = guestOrder(request, data)
    total = float(data["form"]["total"])
    order.transaction_id = transaction_id
    print (total)

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()
    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            town=data['shipping']['town'],
            county=data['shipping']['county'],
            )
    return JsonResponse('Payment complete!', safe=False)

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'store/register_done.html',{'new_user': new_user})
    
    else:
        user_form = UserRegistrationForm()
    return render(request, 'store/register.html',{'user_form': user_form})

def profile(request):
    if request.method == 'POST':
        customer_form = EditProfile(request.POST, instance=request.user.customer)
        if customer_form.is_valid():
            customer_form.save()
            return redirect('profile')
    else:
        customer_form = EditProfile(instance=request.user.customer)
    return render(request, 'store/profile.html', {'customer_form':customer_form})



