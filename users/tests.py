from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserCRUDTests(TestCase):
    fixtures = ['users.json']  # Добавьте эту строку

    def setUp(self):
        self.user = User.objects.get(username='testuser')

    def test_user_registration(self):
        response = self.client.post(reverse('user-create'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после успешной регистрации
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Проверка существования нового пользователя

    def test_user_update(self):
        # Входим в систему перед обновлением
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('user-update', args=[self.user.id]), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updateduser@example.com',
        })
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после успешного обновления
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')  # Проверка обновленного имени пользователя

    def test_user_delete(self):
        # Входим в систему перед удалением
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('user-delete', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после успешного удаления
        self.assertFalse(User.objects.filter(username='testuser').exists())  # Проверка удаления пользователя