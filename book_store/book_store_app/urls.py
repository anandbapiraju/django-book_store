from django.urls import path
from . import views

app_name = 'book_store_app'
urlpatterns=[
    path('',views.BookListView.as_view(),name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/',views.register_view,name='register'),
    path('home/my_profile/',views.my_profile,name='my_profile'),
    path('home/cart/<int:user_id>',views.CartView.as_view(),name='cart'),
    path('home/add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('home/<int:book_id>/',views.book_details_view,name='book_details'),
    path('cart/delete_item/<int:item_id>/',views.delete_item_view,name='delete_item'),
    path('home/update_cart/', views.update_cart_view, name='update_cart'),
    path('home/search/',views.search_view,name='search'),
    path('home/shopping/', views.shopping_view, name='shopping'),
    path('home/order_page/', views.order_page_view, name='order_page'),
    path('home/orders/<int:user_id>/', views.OrdersView.as_view(), name='orders'),
    path('set_language/', views.set_language, name='set_language'),
    path('staff_dashboard/',views.staff_dashboard,name='staff_dashboard'),
    path('staff_dashboard/updateInventory', views.update_inventory_view, name='updateInventory'),
]
