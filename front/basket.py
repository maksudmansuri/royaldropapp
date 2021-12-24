


from django.db.models.fields import DecimalField
# from front.context_processors import basket
from front.models import Product
from decimal import Decimal


class Basket():
    """
        Checkout session stored
    """

    def __init__(self,request):
        self.session = request.session
        basket =self.session.get('skey')
        if 'skey' not in request.session:
            basket = self.session['skey'] ={}
        self.basket = basket 

    def add(self,product,qty):
        product_id=product.id
        if product_id not in self.basket:
            self.basket[product_id] = {'product_mrp':product.product_mrp,'qty':int(qty)}

        self.save()


    def __iter__(self):
        """
        collect the produce_id from session data """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['product_mrp'] = Decimal(item['product_mrp'])
            item['total_price'] = item['product_mrp'] * item['qty'] 
            yield item
        

    def get_total_price(self):
        return sum(Decimal(item['product_mrp']) * item['qty'] for item in self.basket.values())

   

    def delete(self,product):
        """
        Delete Item for session data
        """
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
        
        self.save()


    def save(self):
        self.session.modified =True
