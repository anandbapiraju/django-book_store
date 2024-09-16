from rest_framework import serializers
from ..models import Book, Cart, Profile, Orders, OrderItems, BookSpecifications
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Orders
        fields ='__all__'


class BookSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookSpecifications
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    book_specs = BookSpecificationsSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'book_title', 'author', 'genre', 'price', 'quantity', 'book_img', 'book_specs']


class CartSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, data):
        book = Book.objects.filter(id=data['book_id']).first()
        if not book:
            raise serializers.ValidationError("Book does not exist.")

        if data['quantity'] > book.quantity:
            raise serializers.ValidationError(f"Only {book.quantity} units available for this book.")

        data['book'] = book
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        book = validated_data['book']
        quantity = validated_data['quantity']

        cart_item, created = Cart.objects.get_or_create(user=user, book=book)

        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > book.quantity:
                raise serializers.ValidationError(f"Only {book.quantity - cart_item.quantity} more units available.")
            cart_item.quantity = new_quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        return cart_item

    def update(self, instance, validated_data):
        book = validated_data['book']
        quantity = validated_data['quantity']

        if quantity > book.quantity:
            raise serializers.ValidationError(f"Only {book.quantity} units available for this book.")

        instance.quantity = quantity
        instance.save()
        return instance

