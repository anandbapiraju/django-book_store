from django.urls import path
from . import views

urlpatterns = [
    path('authentication/login/', views.LoginView.as_view(), name="api_login"),
    path('authentication/logout/', views.LogoutView.as_view(), name="api_logout"),
    path('books/book_list/', views.BookListView.as_view(), name="api_book_list"),
    path('books/book_details/<int:pk>/', views.BookDetailView.as_view(), name="api_book_detail"),
    path('cart/cart_list/', views.CartListView.as_view(), name="api_cart_list"),
    path('profile/profile_details/', views.ProfileDetailView.as_view(), name="api_profile_details"),
    path('orders/order_list/', views.OrdersListView.as_view(), name="api_order_list"),
    path('orders/order_items/', views.OrderItemsListView.as_view(), name="api_order_items"),
    path('books/book_specs/<int:pk>/', views.BookSpecificationsDetailView.as_view(), name="api_book_specs"),
    path('cart/add_to_cart/', views.AddToCartView.as_view(), name="api_add_to_cart"),
    path('cart/update_cart/<int:book_id>/', views.UpdateCartView.as_view(), name="api_update_cart"),
    path('cart/delete_cart_item/<int:pk>/', views.DeleteCartItemView.as_view(), name="api_delete_cart_item"),
    path('admin/staff_dashboard/', views.StaffDashboardView.as_view(), name="api_staff_dashboard"),
    path('admin/update_inventory/', views.UpdateInventoryView.as_view(), name="api_update_inventory"),
    path('admin/add_book/', views.AddBookView.as_view(), name="api_add_book"),
    path('admin/delete_book/<int:pk>/', views.DeleteBookView.as_view(), name="api_delete_book"),
    path('admin/book_specs_update/<int:pk>/', views.BookSpecificationsUpdateView.as_view(), name="api_book_specs_update"),
    path('admin/order_history/', views.OrderHistoryView.as_view(), name="api_order_history"),
    path('admin/update_order/<int:pk>/', views.UpdateOrderView.as_view(), name="api_update_order"),
    path('admin/notifications/', views.NotificationsView.as_view(), name="api_notifications"),
]



