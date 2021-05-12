from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from . import models


class CategoryInline(GenericTabularInline):

    model = models.Category


class ProductSpecificationInline(admin.StackedInline):

    model = models.ProductSpecification


class CartProductInline(admin.StackedInline):

    model = models.CartProduct


class DeliveryAddressInline(admin.TabularInline):

    model = models.DeliveryAddress


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):

    inlines = [
        ProductSpecificationInline,
        CategoryInline,
    ]
    list_display = ['name']


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):

    inlines = [
        CartProductInline,
        DeliveryAddressInline,
    ]
    list_display = ['user']


