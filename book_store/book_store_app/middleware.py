from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip the check for the login page and static files
        if request.path.startswith(reverse('book_store_app:login')) or request.path.startswith('/static/') or request.path.startswith(reverse('book_store_app:home')):
            return self.get_response(request)

        # Redirect to login if the user is not authenticated
        if not request.user.is_authenticated:
            return redirect(reverse('book_store_app:login'))

        return self.get_response(request)

