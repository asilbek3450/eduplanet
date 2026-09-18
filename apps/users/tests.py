import tempfile
from pathlib import Path

from django.test import SimpleTestCase, override_settings


class PublicMediaTests(SimpleTestCase):
    def test_uploaded_file_is_available_when_debug_is_disabled(self):
        with tempfile.TemporaryDirectory() as temporary_media_root:
            image_path = Path(temporary_media_root) / 'user_images' / 'avatar.png'
            image_path.parent.mkdir()
            image_path.write_bytes(b'profile-image')

            with override_settings(DEBUG=False, MEDIA_ROOT=temporary_media_root):
                response = self.client.get('/media/user_images/avatar.png')
                content = b''.join(response.streaming_content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, b'profile-image')

    def test_media_route_does_not_allow_directory_traversal(self):
        response = self.client.get('/media/../root/settings.py')

        self.assertEqual(response.status_code, 400)

# Create your tests here.
