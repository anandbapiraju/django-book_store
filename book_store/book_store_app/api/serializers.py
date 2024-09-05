from rest_framework import serializers
from django.shortcuts import get_object_or_404
from ..models import Book, Cart, Profile, Orders, OrderItems, BookSpecifications


class CustomLoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)


class BookSerializer(serializers.ModelSerializer):
    book_img = serializers.ImageField(required=False)

    class Meta:
        model = Book
        fields = ['book_title', 'author', 'genre', 'price', 'quantity', 'book_img']



class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class BookSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSpecifications
        fields = '__all__'


class AddOrUpdateCartSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, data):
        # Ensure the book exists
        book = get_object_or_404(Book, id=data['book_id'])

        # Check if the requested quantity is available
        if data['quantity'] > book.quantity:
            raise serializers.ValidationError(f"Only {book.quantity} units available for {book.title}.")

        # Store the book object in the validated data for use in the create/update methods
        data['book'] = book
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data['book']
        quantity = validated_data['quantity']

        # Create or update the cart item
        cart_item, created = Cart.objects.get_or_create(user=user, book=book)

        # If the item already exists in the cart, update the quantity
        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > book.quantity:
                raise serializers.ValidationError(
                    f"Only {book.quantity - cart_item.quantity} more units available for {book.title}.")
            cart_item.quantity = new_quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        return cart_item

    def update(self, instance, validated_data):
        # Update the existing cart item
        book = validated_data['book']
        quantity = validated_data['quantity']

        # Check if the requested quantity is available for the book
        if quantity > book.quantity:
            raise serializers.ValidationError(f"Only {book.quantity} units available for {book.title}.")

        instance.quantity = quantity
        instance.save()
        return instance


class StaffDashboardSerializer(serializers.Serializer):
    pass
