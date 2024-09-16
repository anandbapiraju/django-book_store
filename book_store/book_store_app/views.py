from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import translation
from django.views.generic import ListView, FormView, UpdateView
from .forms import LoginForm, ProfileForm, BookForm, RegisterForm
from .models import Book, Cart, BookSpecifications, Profile, Orders, OrderItems
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views import View


class BookListView(LoginRequiredMixin,ListView):
    model = Book
    template_name = "book_store_app/home.html"
    context_object_name = 'books'


class CartView(LoginRequiredMixin,ListView):
    model = Cart
    template_name = "book_store_app/cart.html"
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_queryset()
        total_bill = round(sum(item.book.price * item.quantity for item in cart_items), 2)
        context['total_bill'] = total_bill
        return context


class CustomLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'book_store_app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('book_store_app:home')
            else:
                return render(request, 'book_store_app/login.html',
                              {'form': form, 'message': 'Invalid login credentials'})
        return render(request, 'book_store_app/login.html', {'form': form})


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect(reverse('book_store_app:login'))


class RegisterView(FormView):
    template_name = 'book_store_app/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('book_store_app:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        messages.success(self.request, 'Registration successful! You can now log in.')
        return super().form_valid(form)


class MyProfileView(LoginRequiredMixin,UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'book_store_app/my_profile.html'
    success_url = reverse_lazy('book_store_app:home')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


@login_required()
def add_to_cart_view(request):
    if request.method == 'POST':
        units = int(request.POST.get('quantity', 1))
        book_id = int(request.POST.get('book_id'))

        book = get_object_or_404(Book, id=book_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)

        if created:
            if units <= book.quantity:
                cart_item.quantity = units
                cart_item.save()
                request.session['message'] = 'Added to Cart Successfully'
            else:
                request.session['message'] = 'Stock Unavailable'
        else:
            total = cart_item.quantity + units
            if total <= book.quantity:
                cart_item.quantity = total
                cart_item.save()
                request.session['message'] = 'Added to Cart Successfully'
            else:
                request.session['message'] = 'Stock Unavailable'

    return redirect('book_store_app:home')


@login_required
def update_cart_view(request):
    context = {'cart_items': Cart.objects.filter(user=request.user)}
    if request.method == 'POST':
        units = int(request.POST.get('quantity', 1))
        book_id = int(request.POST.get('book_id'))

        book = get_object_or_404(Book, id=book_id)
        cart_item = Cart.objects.get(user=request.user, book=book)
        total = units
        if total <= book.quantity:
            cart_item.quantity = total
            cart_item.save()
            cart_items = Cart.objects.filter(user=request.user)
            total_bill = round(sum(item.book.price * item.quantity for item in cart_items), 4)
            context['total_bill'] = total_bill
        else:
            request.session['message'] = 'Stock Unavailable'

    return render(request, 'book_store_app/cart.html', context)


@login_required
def book_details_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book_specs = get_object_or_404(BookSpecifications, book=book)
    context = {'book_specs': book_specs, 'book': book, }
    return render(request, 'book_store_app/book_details.html', context)


@login_required
def delete_item_view(request, item_id):
    cart = get_object_or_404(Cart, id=item_id, user=request.user)
    cart.delete()
    return redirect('book_store_app:cart', user_id=request.user.id)


@login_required
def search_view(request):
    search_text = ''
    if request.method == 'POST':
        search_text = request.POST.get('text')

        if search_text:
            books = Book.objects.filter(book_title__icontains=search_text)
        else:
            books = Book.objects.none()
    else:
        books = Book.objects.none()
    context = {
        'books': books,
        'search_text': search_text,
    }

    return render(request, 'book_store_app/search_results.html', context)


@login_required
def shopping_view(request):
    profile = Profile.objects.get(user=request.user)
    context = {'profile': profile}
    if request.method == 'POST':
        total_bill = request.POST.get('total_bill')
        print("Received total_bill:", total_bill)
        context['total_bill'] = total_bill

    return render(request, 'book_store_app/shopping.html', context)


@login_required
def checkout_view(request):
    if request.method == 'POST':
        total_bill = request.POST.get('total_bill', '0.0')
        phone_number = request.POST.get('phone_number', '').strip()
        address = request.POST.get('address', '').strip()
        pincode = request.POST.get('pincode', '0').strip()

        if not (phone_number and address and pincode):
            context = {'error': "All fields are required."}
        else:
            order = Orders.objects.create(
                user=request.user,
                total_price=total_bill,
                address=address,
                phone_number=phone_number,
                pincode=int(pincode)
            )

            cart_items = Cart.objects.filter(user=request.user)
            order_items = []
            for item in cart_items:
                order_item = OrderItems.objects.create(
                    user=item.user,
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                )
                order_items.append(order_item)

            cart_items.delete()

            request.session['total_bill'] = total_bill

            context = {
                'total_bill': total_bill,
                'phone_number': phone_number,
                'address': address,
                'pincode': pincode,
                'order_items': order_items,
                'success': "Order placed successfully!"
            }

    return render(request, 'book_store_app/checkout.html', context)


@login_required
def orders_view(request):
    order_items = OrderItems.objects.filter(user=request.user)
    total_bill = request.session.get('total_bill', 0)
    context = {
        'order_items': order_items,
        'total_bill': total_bill
    }
    return render(request, 'book_store_app/orders.html', context)


@login_required
def set_language(request):
    language = request.GET.get('language', '')
    translation.activate(language)
    request.session['django_language'] = language
    return redirect(request.META.get('HTTP_REFERER', '/'))


def staff_login_required(view_func):
    @login_required
    @staff_member_required
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@staff_login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        return redirect('book_store_app:home')

    context = {}
    return render(request, 'book_store_app/inventory/staff_dashboard.html', context)



@staff_login_required
def update_inventory_view(request):
    books = Book.objects.all().order_by('id')
    if request.method == 'POST':
        for book in books:
            book_id = book.id
            book.book_title = request.POST.get(f'book_title_{book_id}')
            book.author = request.POST.get(f'book_author_{book_id}')
            book.genre = request.POST.get(f'book_genre_{book_id}')
            book.price = request.POST.get(f'book_price_{book_id}').replace('$', '')
            book.quantity = request.POST.get(f'book_quantity_{book_id}')
            book.save()
        messages.success(request, 'Inventory updated successfully!')
        return redirect('book_store_app:staff_dashboard')
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_store_app/inventory/updateInventory.html', {'page_obj': page_obj})


@staff_login_required
def add_book_view(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_store_app:staff_dashboard')
    else:
        form = BookForm()

    return render(request, 'book_store_app/inventory/addBook.html', {'form': form})


@staff_login_required
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_store_app:staff_dashboard')


@staff_login_required
def book_specifications_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book_specs = get_object_or_404(BookSpecifications, book=book)
    if request.method == "POST":
        if 'book_img' in request.FILES:
            book.book_img = request.FILES['book_img']
            book.save()
        book_specs.book_code = request.POST.get('book_code')
        book_specs.publisher = request.POST.get('publisher')
        publish_date_str = request.POST.get('publish_date')
        if publish_date_str:
            book_specs.publish_date = datetime.strptime(publish_date_str, '%Y-%m-%d').date()
        book_specs.pages = request.POST.get('pages')
        book_specs.description = request.POST.get('description')
        book_specs.save()
        return redirect('book_store_app:staff_dashboard')
    context = {'book_specs': book_specs}
    return render(request, 'book_store_app/inventory/book_specifications.html', context)


@staff_login_required
def update_order_view(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Orders.objects.get(id=order_id)
            order.address = request.POST.get(f'address_{order_id}')
            order.pincode = request.POST.get(f'pincode_{order_id}')
            order.phone_number = request.POST.get(f'phone_number_{order_id}')
            order.shipping_status = request.POST.get(f'status_{order_id}')
            order.save()
        except Orders.DoesNotExist:
            print("No Order Exists")
            pass
    return redirect('book_store_app:staff_dashboard')


@staff_login_required
def notifications_view(request):
    low_stock_books = Book.objects.filter(quantity__lte=25)
    books_count = low_stock_books.count()
    context = {
        'books': low_stock_books,
        'books_count': books_count
    }
    return render(request, 'book_store_app/inventory/notifications.html', context)


@staff_login_required
def view_inventory(request):
    books_list = Book.objects.all()
    paginator = Paginator(books_list, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'book_store_app/inventory/viewInventory.html', {'page_obj': page_obj})


@staff_login_required
def view_orders(request):
    status_filter = request.GET.get('status', '')

    if status_filter:
        orders = Orders.objects.filter(shipping_status=status_filter.capitalize())
    else:
        orders = Orders.objects.all()

    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'book_store_app/inventory/viewOrders.html', context)


@staff_login_required
def order_status_view(request):
    # Get all orders
    orders = Orders.objects.all()

    if request.method == 'POST':
        for order in orders:
            # Update the shipping status based on the form input
            status = request.POST.get(f'order_status_{order.id}')
            order.shipping_status = status
            order.save()

        return redirect('book_store_app:orderStatus')  # Redirect after updating

    context = {
        'orders': orders
    }
    return render(request, 'book_store_app/inventory/order_status.html', context)
