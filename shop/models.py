from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class Category(models.Model):

    tag = models.SlugField(unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.tag


class Product(models.Model):

    tags = GenericRelation(Category, related_query_name='product')
    name = models.CharField(max_length=60)
    image = models.ImageField()
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):

    UNIT_CHOICES = [('PC', 'Piece'), ('PK', 'Pack'), ('PR', 'Pair'),
                    ('BX', 'Box'), ('LT', 'Lot')]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature_name = models.CharField(max_length=40)
    image = models.ImageField()
    characteristic = models.TextField(null=True)
    unit_of_measure = models.CharField(max_length=2, choices=UNIT_CHOICES)
    available_quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.product}: {self.feature_name}'


class Account(models.Model):

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # quantity_in_cart = models.PositiveIntegerField(default=0)
    # value_of_cart = models.DecimalField(
    #     max_digits=9, decimal_places=2, default=0.00,
    # )

    def __str__(self):
        return f"{self.user}'s account"


class CartProduct(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    product_specification = models.ForeignKey(
        ProductSpecification, on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.product_specification} in cart'

    def quantity_in_cart(self):
        pass

    def value_of_cart(self):
        pass


class DeliveryAddress(models.Model):

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=90)
    country = models.CharField(max_length=60)
    region = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    postcode = models.CharField(max_length=10)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.full_name}'s address"
