from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from phone_field import PhoneField
#from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    #email = models.EmailField()
    phone = PhoneField(blank=True, help_text='Contact phone number', max_length=20, default="",E164_only=False)

    def __str__(self):
        full_name = self.first_name + " " + self.last_name
        return full_name

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, null=True, default='')
    slug = models.SlugField(max_length=200, unique=True, null=True, default='')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('sandle_list_by_category', 
        args=[self.slug])

class Size(models.Model):
    category = models.ManyToManyField(Category, related_name="sizes")
    size = models.CharField(max_length=50, null=True, blank=True, default='')

    def __str__(self):
        return "Size " + self.size

class Sandle(models.Model):
    category = models.ForeignKey(Category, related_name='products',
               on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, db_index=True, default='')
    price = models.DecimalField(max_digits=6, decimal_places=0)
    digital = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(blank=True)
    image= models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sandle_detail', args=[self.id, self.slug])

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.sandle.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    sandle = models.ForeignKey(Sandle, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, default='')
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sandle.name

    @property
    def get_total(self):
        total = self.sandle.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    county = models.CharField(max_length=200, null=False)
    town = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    def transaction_id(self):
        return self.order.transaction_id

def set_username(sender, instance, **kwargs):
    instance.username = instance.email
models.signals.pre_save.connect(set_username, sender=User)



