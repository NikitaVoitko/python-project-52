from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Status

User = get_user_model()


class StatusCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.status = Status.objects.create(name='Old Status')

    def test_status_create(self):
        response = self.client.post(reverse('status-create'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update(self):
        response = self.client.post(
            reverse('status-update', args=[self.status.id]),
            {'name': 'Updated Status'}
        )
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_delete(self):
        response = self.client.post(reverse('status-delete', args=[self.status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(name='Old Status').exists())
