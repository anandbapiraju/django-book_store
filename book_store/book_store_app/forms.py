from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Book, Orders


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


class RegisterForm(forms.ModelForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2




class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=False
    )
    email = forms.EmailField(
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.username
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
        self.user = user

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        # Update user details
        if self.user:
            if 'first_name' in self.cleaned_data and self.cleaned_data['first_name']:
                self.user.first_name = self.cleaned_data['first_name']
            if 'last_name' in self.cleaned_data and self.cleaned_data['last_name']:
                self.user.last_name = self.cleaned_data['last_name']
            if 'email' in self.cleaned_data and self.cleaned_data['email']:
                self.user.email = self.cleaned_data['email']
            self.user.save()
        return profile

    class Meta:
        model = Profile
        fields = ['phone_number', 'gender', 'address']
        # Ensure that fields from the Profile model are optional by setting blank=True in model definition



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

