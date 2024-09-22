# utils.py
from django.contrib import messages

def add_message(request, level, message):
    """Add a message of a specific level to the request."""
    levels = {
        'success': messages.success,
        'error': messages.error,
        'warning': messages.warning,
        'info': messages.info,
    }
    levels.get(level, messages.info)(request, message)
