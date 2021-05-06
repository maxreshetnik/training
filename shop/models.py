from django.db import models
from django.contrib.auth import get_user_model


# 1 Category
# 2 Product
# 3 ProductSpecification
# 4 Cart
# 5 CartProduct
# 6 Customer
# *******************
# 7 Order

class Category(models.Model):

    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=60)
    image = models.ImageField()
    description = models.TextField(null=True)

    def __str__(self):
        return self.title


class ProductSpecification(models.Model):

    UNIT_CHOICES = [('PC', 'Piece'), ('PK', 'Pack'), ('PR', 'Pair'),
                    ('BX', 'Box'), ('LT', 'Lot')]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=60)
    image = models.ImageField()
    characteristic = models.TextField(null=True)
    unit_of_measure = models.CharField(max_length=2, choices=UNIT_CHOICES)
    available_quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.product.title}: {self.feature_name}'


class Cart(models.Model):

    user = models.OneToOneField(get_user_model())
    quantity_in_cart = models.PositiveIntegerField(default=0)
    value = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s cart"


class CartProduct(ProductSpecification):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.product.title}: {self.feature_name} in cart'


class Customer(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=90)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'Customer: {self.full_name}'
