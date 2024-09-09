from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Initialize the DefaultRouter
router = DefaultRouter()

router.register(r'books', views.BookViewSet, basename='book')
router.register(r'book-specs', views.BookSpecViewSet, basename='book_spec')
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'cart', views.CartViewSet, basename='cart')
router.register(r'staff-dashboard', views.StaffDashboardViewSet, basename='staff_dashboard')
router.register(r'logout', views.LogoutViewSet, basename='logout')


# Custom URLs that are not handled by viewsets
urlpatterns = [
    path('authentication/login/', views.LoginView.as_view(), name='api_login'),
    path('authentication/register/', views.RegisterView.as_view(), name='api_register'),
    path('profile/profile_details/', views.ProfileDetailView.as_view(), name="api_profile_details"),
    path('books/book_details/<int:pk>/', views.BookViewSet.as_view({'get': 'retrieve'}), name='api_book_detail'),
    path('cart/update_cart/<int:book_id>/', views.CartViewSet.as_view({'put': 'update'}), name='api_update_cart'),
    path('cart/delete_cart_item/<int:pk>/', views.CartViewSet.as_view({'delete': 'destroy'}), name='api_delete_cart_item'),
    path('admin/add_book/', views.BookViewSet.as_view({'post': 'create'}), name='api_add_book'),
    path('admin/update_book/<int:pk>', views.BookViewSet.as_view({'put': 'update_book'}), name='api_update_book'),
    path('admin/update_book/<int:pk>', views.BookViewSet.as_view({'patch': 'update_book'}), name='api_update_book'),
    path('admin/delete_book/<int:pk>/', views.BookViewSet.as_view({'delete': 'delete_book'}), name='api_delete_book'),
    path('admin/book_specs_update/<int:pk>/', views.BookSpecViewSet.as_view({'put': 'update'}), name='api_book_specs_update'),
    path('admin/order_history/', views.OrderViewSet.as_view({'get': 'list'}), name='api_order_history'),
    path('admin/update_order/<int:pk>/', views.OrderViewSet.as_view({'put': 'update_order'}), name='api_update_order'),
    path('admin/notifications/', views.StaffDashboardViewSet.as_view({'get': 'notifications'}), name='api_notifications'),
    path('orders/order_status/',views.OrderStatusAPIView.as_view(),name='api_order_status')
]


urlpatterns += router.urls
