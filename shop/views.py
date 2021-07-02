from django.http import Http404
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.contenttypes.models import ContentType
from django.db.models import (Prefetch, F, Min, Max, Avg,
                              Subquery, Count, OuterRef, Exists)

from .models import Category, Specification, Rate


def layout_view(request):
    return render(request, 'shop/layout.html', {})


class ShopView(TemplateView):

    template_name = 'shop/home.html'
    catalog = Category.objects.filter(
        category__isnull=True
    ).prefetch_related(
        Prefetch('categories', to_attr='subcategories')
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catalog'] = self.catalog
        context['navbar_template_name'] = 'shop/navbar.html'
        context['rating_scale'] = [
            (n - 0.2, n - 0.75) for n in Rate.PointValue.values
        ]
        return context


class HomePageView(ShopView):

    def get_queryset(self):
        rate_subquery = Rate.objects.filter(
            content_type_id=OuterRef('content_type_id'),
            object_id=OuterRef('object_id'),
        ).order_by().values('object_id').annotate(Avg('point'))

        queryset = Specification.objects.filter(
            available_qty__gt=0,
        ).order_by('-id').annotate(
            rating=Subquery(rate_subquery.values('point__avg')),
        ).prefetch_related(
            Prefetch('content_object', to_attr='product')
        )
        return queryset[:4]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = self.get_queryset()
        return context


class CategorySpecList(MultipleObjectMixin, ShopView):

    template_name = 'shop/specs_by_category.html'
    context_object_name = 'spec_list'
    object_list = None
    # paginate_by = 5

    def get_category(self):
        # category = Category.objects.select_related('category')
        try:
            category = self.catalog.get(
                name__iexact=self.kwargs['category'],
            )
        except Category.DoesNotExist:
            raise Http404("No category matches the given name.")
        self.kwargs['category'] = category
        return category

    def get_product_subquery(self):
        products = ContentType.objects.get_for_id(
            self.kwargs['category'].content_type_id
        ).model_class().objects.filter(
            id=OuterRef('object_id'),
        ).order_by().values('category__name')

        return products

    def get_queryset(self):

        category = self.get_category()
        ct_id = category.content_type_id

        rate_subquery = Rate.objects.filter(
            content_type_id=OuterRef('content_type_id'),
            object_id=OuterRef('object_id'),
        ).order_by().values('object_id').annotate(Avg('point'))

        queryset = Specification.objects.filter(
            content_type_id=ct_id, available_qty__gt=0,
        ).annotate(
            category_name=Subquery(self.get_product_subquery()),
        ).filter(
            category_name__isnull=False,
        ).annotate(
            rating=Subquery(rate_subquery.values('point__avg')),
        ).prefetch_related(
            Prefetch('content_object', to_attr='product')
        )

        # for q in queryset:
        #     print(q.discount_price)
        #
        # print(queryset)

        return queryset

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        return context


class SubcategorySpecList(CategorySpecList):

    def get_category(self):
        category = Category.objects.select_related('category')
        try:
            category = category.get(
                name__iexact=self.kwargs['subcategory'],
            )
        except Category.DoesNotExist:
            raise Http404("No subcategory matches the given name.")
        self.kwargs['category'] = category
        return category

    def get_product_subquery(self):
        products = super().get_product_subquery()
        products = products.filter(category=self.kwargs['category'])
        return products


class ProductList(MultipleObjectMixin, ShopView):

    template_name = 'shop/products_by_category.html'
    context_object_name = 'product_list'
    object_list = None

    def get_queryset(self):
        category = Category.objects.select_related('category')
        category = category.prefetch_related(
            Prefetch('categories', to_attr='subcategories'),
        )
        try:
            category = category.get(
                name__iexact=self.kwargs['category'],
            )
        except Category.DoesNotExist:
            raise Http404("No category matches the given name.")
        self.kwargs['category'] = category

        product_model = ContentType.objects.get_for_id(
            category.content_type_id
        ).model_class()

        queryset = product_model.objects.filter(
            specs__available_qty__gt=0,
        ).select_related('category')

        if not category.subcategories:
            queryset = queryset.filter(category_id=category.id)
        # elif category.category_id is not None:
        #     queryset = queryset.filter(
        #         category__in=category.subcategories
        #     )
        # specs = Specification.objects.filter(
        #     content_type_id=category.content_type_id,
        # ).annotate(
        #     min_price=Case(
        #         When(discount_price__gt=0, then='discount_price'),
        #         default='price'
        #     ),
        # ).order_by('discount_price')
        #
        spec_sale = Specification.objects.filter(
            object_id=OuterRef('pk'),
            discount_price__lt=F('price')
        )

        queryset = queryset.annotate(
            min_discount_price=Min('specs__discount_price'),
            min_price=Min('specs__price'),
            max_discount_price=Max('specs__discount_price'),
            specs_count=Count('specs'),
            sale=Exists(spec_sale),
            rating=Avg('rates__point'),
        )
        # for q in queryset:
        #     print(q.min_discount_price)
        #     print(q.min_price)
        #     print(q.max_discount_price)
        #     print(q.sale)

        return queryset

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        return context


class ProductDetail(DetailView):
    pass
