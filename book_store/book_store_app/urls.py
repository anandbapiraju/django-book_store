from django.urls import path
from . import views

app_name = 'book_store_app'
urlpatterns=[
    path('',views.BookListView.as_view(),name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/',views.register_view,name='register'),
    path('my_profile/',views.my_profile,name='my_profile'),
    path('cart/',views.CartView.as_view(),name='cart'),
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('<int:book_id>/',views.book_details_view,name='book_details'),


]
