from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('home/', views.base, name='home'),
    path('orders/', views.orders, name='orders'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('orders/', views.orders, name='orders'),
    path('add_payment_method/', views.add_payment_method, name='add_payment_method'),
    path('buy_gift_card/', views.buy_gift_card, name='buy_gift_card'),
    path('initiate-payment/<int:sale_id>/<int:selling_price>', views.initiate_payment, name='initiate_payment'),
    path('buy_gift_card/<int:card_id>/<int:selling_price>', views.buy_gift_card_item, name='buy_gift_card'),
    path('sell_gift_card/', views.sell_gift_card, name='sell_gift_card'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('payment-success/', views.success_page, name='success_page'),
    path('sale-payment-success/', views.sale_success_page, name='sale_success'),
    path('get-payment-methods/<int:id>/', views.get_payment_methods, name='payment_mode_id'),
]
