from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Div, Layout
from django.urls import reverse

from .models import Profile, Book, Orders


class LoginForm(forms.Form):

    username = forms.CharField(
            label="UserName",
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
        self.helper.form_action = reverse('book_store_app:login')


class RegisterForm(forms.Form):
    username = forms.CharField(
        label="UserName",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    email = forms.CharField(
        label="Email",
        max_length=256,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password Again'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
        self.helper.form_action = reverse('book_store_app:register')



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                'first_name',
                'last_name',
                'email',
                'gender',
                'address',
                'phone_number',
                css_class='form-group'
            ),
            Div(
                Submit('submit', 'Update Profile', css_class='btn btn-primary'),
                HTML('<a href="{% url "book_store_app:home" %}" class="btn btn-secondary">Cancel</a>'),
                css_class='form-group'
            )
        )
        self.helper.form_action = "/home/my_profile/"

        if self.instance and hasattr(self.instance, 'user'):
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'gender', 'address', 'phone_number']
        widgets = {
            'gender': forms.Select(choices=[]),
        }


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

