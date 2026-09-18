"""Public media delivery for deployments without a web-server media route.

In production a reverse proxy or object storage/CDN can take over this URL.
Keeping this small fallback makes locally persisted uploads available when
``DEBUG`` is disabled (for example under Passenger).
"""
from django.conf import settings
from django.http import Http404, HttpResponseNotFound
from django.views.static import serve


def public_media(request, path):
    """Serve a file below MEDIA_ROOT with Django's traversal protection."""
    try:
        return serve(request, path, document_root=settings.MEDIA_ROOT)
    except Http404:
        return HttpResponseNotFound('Media file not found.')
