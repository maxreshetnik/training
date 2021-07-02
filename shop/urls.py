from django.urls import path

from . import views


app_name = 'shop'
urlpatterns = [
    path('layout/', views.layout_view, name='layout'),
    path('', views.HomePageView.as_view(), name='home'),
    path('<category>/', views.CategorySpecList.as_view(),
         name='category'),
    path('<category>/new', views.CategorySpecList.as_view(),
         name='new'),
    path('<category>/popular', views.CategorySpecList.as_view(),
         name='popular'),
    path('<category>/<subcategory>/',
         views.SubcategorySpecList.as_view(), name='subcategory'),
    # path('<category>/products/', views.ProductList.as_view(),
    #      name='products'),
    path('<int:ct_id>/<int:pk>/', views.ProductDetail.as_view(),
         name='product_detail'),
]
