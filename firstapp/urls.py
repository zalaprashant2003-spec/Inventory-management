from django.urls import path
from . import views
app_name = "firstapp"

urlpatterns = [
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("", views.home, name="home"),
    path("logout/", views.logout_request, name="logout"),
    path("create/", views.create_item, name='create_item'),
    path('list/', views.list_item, name='list_item'),
    path('item_less_than/', views.item_less_than, name='item_less_than'),
    path('list_customer/', views.list_customer, name='list_customer'),
    path('<int:id>/',views.detail_item, name='detail_item'),
    path('<int:id>/update/',views.update_item, name='update_item'),
    path('<int:id>/delete/',views.delete_item, name='delete_item'),
    path('<str:customer>/alltime_purchase/',views.alltime_purchase, name='alltime_purchase'),
    path('<str:customer>/bill/',views.bill, name='bill'),
    path("orders/", views.order_page, name="order_page"),
    path("orders/add/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("orders/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("orders/update/", views.update_cart, name="update_cart"),
    path("orders/checkout/", views.checkout, name="checkout"),  
    path("customer_bill/", views.customer_bill, name="customer_bill"),
    path("customer/alltime/", views.customer_alltime, name="customer_alltime"),  
    path('add',views.add,name='add'),
    path('sub',views.sub,name='sub'),
]

