from django.urls import path

from . import views


app_name = 'shop'

urlpatterns = [
    # path('layout/', views.layout_view, name='layout'),
    path('', views.HomePageView.as_view(), name='home'),
    path('<category>/', views.CategorySpecList.as_view(),
         name='category'),
    path('<category>/new/', views.NewArrivalsSpecList.as_view(),
         name='new'),
    path('<category>/popular/', views.PopularSpecList.as_view(),
         name='popular'),
    path('<category>/<subcategory>/',
         views.SubcategorySpecList.as_view(), name='subcategory'),
    path('<category>/<subcategory>/<int:pk>/',
         views.SpecificationDetail.as_view(), name='spec_detail'),
    # path('<category>/products/',
    #      views.ProductList.as_view(), name='products'),
]
