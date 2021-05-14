from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from . import models


class CategoryInline(GenericTabularInline):

    model = models.Category
    extra = 1


class ProductSpecificationInline(admin.StackedInline):

    model = models.ProductSpecification
    extra = 1


class CartProductInline(admin.StackedInline):

    model = models.CartProduct
    extra = 0


class ShippingAddressInline(admin.StackedInline):

    model = models.ShippingAddress
    extra = 1


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
        ShippingAddressInline,
    ]
    list_display = ['user']


admin.site.register(models.Category, admin.ModelAdmin)
