from django.contrib.auth.models import User
from django.db import models



class Profile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Male = 'Male'
    Female = 'Female'
    Other = 'Other'
    GENDER_CHOICES = [
        (Male, 'Male'),
        (Female, 'Female'),
        (Other, 'Other')
    ]
    gender = models.CharField(max_length=12, choices=GENDER_CHOICES, default=Other)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'


class Book(models.Model):
    objects = models.Manager()
    book_title = models.CharField(max_length=256)
    author = models.CharField(max_length=256)
    genre = models.CharField(max_length=256)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)
    book_img = models.ImageField(upload_to='book_store_app/images')

    def __str__(self):
        return self.book_title


class BookSpecifications(models.Model):
    objects = models.Manager()
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    book_code = models.CharField(max_length=256)
    publisher = models.CharField(max_length=256)
    publish_date = models.DateField(null=True)
    pages= models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)


class Cart(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=0)


    def __str__(self):
        return f"{self.user}'s cart: {self.book} (Quantity: {self.quantity})"



class Orders(models.Model):
    DoesNotExist = None
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_price = models.FloatField(default=0.0)
    address = models.CharField(max_length=256,null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    pincode = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    SHIPPING_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
    ]
    shipping_status = models.CharField(
        max_length=10,
        choices=SHIPPING_STATUS_CHOICES,
        default='pending',
    )

    def __str__(self):
        return f"Order  by {self.user} at {self.time}"



class OrderItems(models.Model):
    objects = models.Manager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order_items')
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book,on_delete=models.CASCADE, related_name='order_items')
    quantity = models.IntegerField(default=1)

