from django.contrib import admin
from django.urls import path
from store.views import show_product,checkout,add_to_cart,home,cart,order,login,logout,signup
from store.views import validatePayment

urlpatterns = [
    path('', home , name='homepage'),
    path('cart/', cart),
    path('order/', order,name='order'),
    path('login/', login,name='login'),
    path('logout/', logout),
    path('signup/', signup),
    path('checkout/', checkout),
    path('product/<str:slug>', show_product),
    path('addtocart/<str:slug>/<str:active_size>', add_to_cart),
    path('validate_payment', validatePayment),
]