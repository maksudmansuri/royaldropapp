from email.policy import default
from django.db import models

from front.models import Product
from accounts.models import Customers,CustomUser

# Create your models here.


class Cart(models.Model):
    customer = models.ForeignKey(Customers, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.customer,
                                               self.item,
                                               self.quantity,
                                               self.created_at,
                                               self.updated_at)


class DeliveryCost(models.Model):
    status = models.CharField(max_length=7,
                              choices=(('Active', 'active'), ('Passive', 'passive')),
                              default="passive",null=True,blank=True)
    cost_per_delivery = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True,default=0.0)
    cost_per_product = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True,default=0.0)
    fixed_cost = models.DecimalField(max_digits=10, decimal_places=2, null=False,blank=True,default=0.0)
    state_name = models.CharField(max_length=50,null=True,blank=True,default="")
    cost_kg    = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True,default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.status,
                                                    self.cost_per_delivery,
                                                    self.cost_per_product,
                                                    self.state_name,
                                                    self.cost_kg,
                                                    self.fixed_cost,
                                                    self.created_at,
                                                    self.updated_at)
