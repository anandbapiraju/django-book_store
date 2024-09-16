from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import viewsets, permissions, status,generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from ..models import Book, Cart, BookSpecifications, Profile, Orders, OrderItems
from .serializers import (
    BookSerializer, CartSerializer, BookSpecificationsSerializer,
    ProfileSerializer, OrdersSerializer, LoginSerializer,
    RegisterSerializer, OrderItemsSerializer,
)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class LogoutViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Book.objects.all()
        return Book.objects.filter(quantity__gt=0)

    @action(detail=True, methods=['put'], name='update_book')
    def update_book(self, request, pk=None):
        if self.request.user.is_staff:
            book = self.get_object()
            serializer = self.get_serializer(book, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['delete'], name='delete_book')
    def delete_book(self, request, pk=None):
        if self.request.user.is_staff:
            book = self.get_object()
            book.delete()
            return Response({"message": "Book deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "Unauthorized access"}, status=status.HTTP_401_UNAUTHORIZED)


class BookSpecViewSet(viewsets.ModelViewSet):
    queryset = BookSpecifications.objects.all()
    serializer_class = BookSpecificationsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        required_fields = ['total_price', 'address', 'phone_number', 'pincode']
        if not all(request.data.get(field) for field in required_fields):
            return Response({'message': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        order = Orders.objects.create(
            user=self.request.user,
            total_price=request.data['total_price'],
            address=request.data['address'],
            phone_number=request.data['phone_number'],
            pincode=request.data['pincode'],
        )
        cart_items = Cart.objects.filter(user=self.request.user)
        for item in cart_items:
            OrderItems.objects.create(
                user=item.user,
                order=order,
                book=item.book,
                quantity=item.quantity,
            )
        cart_items.delete()
        return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'], name='update_order')
    def update_order(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['get'], name='order_items')
    def order_items(self, request, pk=None):
        order = self.get_object()
        order_items = OrderItems.objects.filter(order=order)
        serializer = OrderItemsSerializer(order_items, many=True)
        return Response(serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        else:
            return Cart.objects.none()


class StaffDashboardViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def list(self, request):
        return Response({"message": "Staff dashboard"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], name='notifications')
    def notifications(self, request):
        low_stock_books = Book.objects.filter(quantity__lte=25)
        books_count = low_stock_books.count()
        return Response({
            'books': BookSerializer(low_stock_books, many=True).data,
            'books_count': books_count
        })

    @action(detail=False, methods=['get'], name='view_inventory')
    def view_inventory(self, request):
        books = Book.objects.all()
        paginator = Paginator(books, 10)
        page = paginator.get_page(request.query_params.get('page', 1))
        serializer = BookSerializer(page, many=True)
        return Response({
            'books': serializer.data,
            'total_pages': paginator.num_pages,
            'current_page': page.number
        })


class OrderStatusAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):

        orders = Orders.objects.all()
        serializer = OrdersSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        order_updates = request.data.get('orders', [])

        for order_data in order_updates:
            order_id = order_data.get('order_id')
            status_value = order_data.get('shipping_status')

            if order_id and status_value:
                try:
                    order = Orders.objects.get(id=order_id)
                    order.shipping_status = status_value
                    order.save()
                except Orders.DoesNotExist:
                    return Response({"message": f"Order {order_id} not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Shipping statuses updated successfully"}, status=status.HTTP_200_OK)
