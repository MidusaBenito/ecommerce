from .models import Category
from . utils import cookieCart, cartData
def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}

def cart_items(request):
    data = cartData(request)
    cartItems = data['cartItems']
    return {'cartItems': cartItems}