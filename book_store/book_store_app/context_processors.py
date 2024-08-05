from django.utils.translation import get_language


def current_language(request):
    return {
        'current_language': get_language(),
    }
