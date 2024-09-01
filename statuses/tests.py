from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status  # Импорт модели Status из текущего приложения


class StatusCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_status_create(self):
        response = self.client.post(reverse('status-create'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_status_update(self):
        status = Status.objects.create(name='Old Status')
        response = self.client.post(reverse('status-update', args=[status.id]), {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)
        status.refresh_from_db()
        self.assertEqual(status.name, 'Updated Status')

    def test_status_delete(self):
        status = Status.objects.create(name='Delete Status')
        response = self.client.post(reverse('status-delete', args=[status.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(name='Delete Status').exists())