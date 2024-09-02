from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCRUDTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='password123',
            first_name='First',
            last_name='Last'
        )

    def test_user_registration_success(self):
        response = self.client.post(reverse('user-create'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'first_name': 'First',
            'last_name': 'Last'
        })
        # Проверяем, что произошел редирект после успешной регистрации
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_failure(self):
        response = self.client.post(reverse('user-create'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'differentpassword123',
            'first_name': 'First',
            'last_name': 'Last'
        })
        # Проверяем, что страница возвращает ошибку (например, статус 200 и сообщение об ошибке)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match.")
        self.assertFalse(User.objects.filter(username='newuser').exists())

    def test_user_update(self):
        # Логинимся под пользователем используя force_login
        self.client.force_login(self.user)
        
        response = self.client.post(reverse('user-update', args=[self.user.id]), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User'
        })
        # Проверяем, что произошел редирект после успешного обновления
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_delete(self):
        # Логинимся под пользователем используя force_login
        self.client.force_login(self.user)
        
        response = self.client.post(reverse('user-delete', args=[self.user.id]))
        # Проверяем, что произошел редирект после успешного удаления
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='testuser').exists())