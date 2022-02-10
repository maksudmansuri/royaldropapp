import json
from accounts.models import Customers
from cart.models import Cart
from .basket import Basket


def basket(request):
    return {'basket':Basket(request)}

def cartProduct(request):
    cartproducts = 0 
    if request.user.user_type == 3:
        cartproducts = Cart.objects.filter(customers = request.user.customers)
        for item in cartproducts:
            response = json.dumps(cartproducts,default=str)      
    return {'cartproducts':response}