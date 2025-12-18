from django.urls import path

from . import views

urlpatterns = [
    path('', views.userhome),
    path('cpuser/', views.cpuser),
    path('epuser/', views.epuser),
    path('makecharity/', views.makecharity),
    path('payment/', views.payment),
    path('success/', views.success),
    path('cancel/', views.cancel),
    path("searchproduct/", views.searchproduct),
    path("viewsubcategory/", views.viewsubcategory),
    path("addproduct/", views.addproduct),
    path("viewproduct/", views.viewproduct),
    
    #
    path("products/", views.products, name="products"),
    # path("product/<int:pid>/", views.product_detail, name="product_detail"),
    # path('products/<int:pid>/bid/', views.bid_product, name='bid_product'), #
    path("products/", views.products, name="products"),
    path("product/<int:pid>/", views.product_detail, name="product_detail"),
    path('products/<int:pid>/bid/', views.bid_product, name='bid_product'), 
   

]
