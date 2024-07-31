from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login
from django.urls import reverse
from django.views.generic import ListView

from .forms import LoginForm, RegisterForm, ProfileForm
from .models import Book, Cart

User = get_user_model()


class BookListView(ListView):
    model=Book
    template_name="book_store_app/home.html"
    context_object_name='books'


class CartView(ListView):
    model = Cart
    template_name = "book_store_app/cart.html"
    context_object_name = 'cart_items'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)



def login_view(request):
    context={'form': LoginForm()}
    if request.method == 'POST':
        print("login view is called..... post method called")
        print('request_method==>', request.POST)
        user_name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            context['current_user']=request.user
            return redirect('book_store_app:home')
        else:
            context['message']= 'Invalid login credentials'
    else:
        print("login view is called..... get method called")
    return render(request, 'book_store_app/login.html', context)


def logout_view(request):
    request.session.flush()
    return redirect(reverse("book_store_app:login"))


def register_view(request):
    context={'form':RegisterForm()}
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if password1 != password2:
                context['message']='Password Mismatch!!'
            elif User.objects.filter(username=user_name).exists():
                context['message']='User Already Exists'
            else:
                User.objects.create_user(username=user_name, email=email, password=password1)
                messages.success(request, 'Account created successfully! Login Here')
                return redirect('book_store_app:login')

    return render(request, 'book_store_app/register.html', context)



@login_required(login_url='book_store_app:login')
def my_profile(request):
    user = request.user
    profile=user.profile
    if request.method=='POST':
        form =ProfileForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            print(profile.gender)
            return redirect('book_store_app:home')
    else:
        form = ProfileForm(instance=profile)
    context = {
        'user': user,
        'form': form
    }
    return render(request, 'book_store_app/my_profile.html', context)





@login_required(login_url='book_store_app:login')
def add_to_cart_view(request):
    if request.method=='POST':
        units=int(request.POST.get('quantity',1))
        book_id=int(request.POST.get('book_id'))

        book= get_object_or_404(Book,id=book_id)


        if book.quantity>=units:
            c=Cart.objects.filter(book=book)
            Cart.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'quantity': c.quantity+units}
            )

            request.session['message']='Added to Cart Successfully'
        else:
            request.session['message']='Stock Unavailable'


    return redirect('book_store_app:home')



@login_required(login_url='book_store_app:login')
def book_details_view(request,book_id):
    book = get_object_or_404(Book, id=book_id)
    context = {'book': book}
    return render(request,'book_store_app/book_details.html',context)
