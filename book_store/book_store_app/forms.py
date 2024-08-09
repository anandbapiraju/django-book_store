from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Div, Layout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

from .models import Profile, Book, Orders


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Login'))

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    last_name = forms.CharField(max_length=30,required=False)
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
        self.user = user


    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        # Update user details
        if self.user:
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            self.user.email = self.cleaned_data['email']
            self.user.save()
        return profile

    class Meta:
        model = Profile
        fields = ['phone_number', 'gender', 'address']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['id','book_title', 'author', 'genre', 'price', 'quantity','book_img']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['book_title'].widget.attrs.update({'class': 'form-control'})
        self.fields['author'].widget.attrs.update({'class': 'form-control'})
        self.fields['genre'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['book_img'].widget.attrs.update({'class': 'form-control'})



class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['shipping_status']

