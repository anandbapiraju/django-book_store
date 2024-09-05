from django.contrib.auth import authenticate
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *


class LoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer
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


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if getattr(self, 'swagger_fake_view', False):
            # Bypass the logout logic during schema generation
            return Response(status=status.HTTP_200_OK)

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BookListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CartListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)


class OrdersListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrdersSerializer

    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)


class OrderItemsListView(generics.ListAPIView):
    serializer_class = OrderItemsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItems.objects.filter(user=self.request.user)


class BookSpecificationsDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = BookSpecifications.objects.all()
    serializer_class = BookSpecificationsSerializer


class AddToCartView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddOrUpdateCartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_item = serializer.save()
        request.session['message'] = 'Added to Cart Successfully'
        return Response({"message": "Added to cart successfully"}, status=201)


class UpdateCartView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AddOrUpdateCartSerializer

    def get_object(self):
        book_id = self.kwargs.get('book_id')
        cart_item = get_object_or_404(Cart, user=self.request.user, book_id=book_id)
        return cart_item

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart_item = self.get_object()
        self.perform_update(serializer)
        return Response({"message": "Cart updated successfully"}, status=200)


class DeleteCartItemView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=204)


class StaffDashboardView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = StaffDashboardSerializer

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"detail": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "Staff dashboard"}, status=status.HTTP_200_OK)


class UpdateInventoryView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def put(self, request, *args, **kwargs):
        books_data = request.data
        for book_data in books_data:
            book_id = book_data.get('id')
            book = get_object_or_404(Book, id=book_id)
            serializer = self.get_serializer(book, data=book_data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        return Response({"message": "Inventory updated successfully"}, status=status.HTTP_200_OK)


class AddBookView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class DeleteBookView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            book = self.get_object()

        except NotFound:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        book.delete()

        return Response({"message": "Book deleted successfully"}, status=status.HTTP_200_OK)


class BookSpecificationsUpdateView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = BookSpecifications.objects.all()
    serializer_class = BookSpecificationsSerializer


class OrderHistoryView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = OrdersSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to access this resource.")
        return Orders.objects.all().order_by('-id')


class UpdateOrderView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": "Order updated successfully"}, status=status.HTTP_200_OK)


class NotificationsView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(quantity__lte=25)
