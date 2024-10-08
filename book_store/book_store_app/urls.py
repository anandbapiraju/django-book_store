from django.urls import path
from . import views

app_name = 'book_store_app'
urlpatterns=[
    path('',views.BookListView.as_view(),name="home"),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('home/my_profile/',views.MyProfileView.as_view(),name='my_profile'),
    path('home/cart/<int:user_id>',views.CartView.as_view(),name='cart'),
    path('home/add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('home/<int:book_id>/',views.book_details_view,name='book_details'),
    path('cart/delete_item/<int:item_id>/',views.delete_item_view,name='delete_item'),
    path('home/update_cart/', views.update_cart_view, name='update_cart'),
    path('home/search/',views.search_view,name='search'),
    path('home/shopping/', views.shopping_view, name='shopping'),
    path('home/checkout/', views.checkout_view, name='checkout'),
    path('home/orders/<int:user_id>/', views.OrdersView.as_view(), name='orders'),
    path('set_language/', views.set_language, name='set_language'),
    path('staff_dashboard/',views.staff_dashboard,name='staff_dashboard'),
    path('staff_dashboard/updateInventory/', views.update_inventory_view, name='updateInventory'),
    path('staff_dashboard/order_history/', views.order_history_view, name='order_history'),
    path('staff_dashboard/update_order/', views.update_order_view, name='update_order'),
    path('staff_dashboard/addBook/', views.add_book_view, name='addBook'),
    path('staff_dashboard/deleteBook/<int:book_id>/', views.delete_book_view, name='deleteBook'),
    path('staff_dashboard/book_specifications/<int:book_id>/', views.book_specifications_view, name='book_specifications'),
    path('staff_dashboard/notifications', views.notifications_view, name='notifications' ),
]
