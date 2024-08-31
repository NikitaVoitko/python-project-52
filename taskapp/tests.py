from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status, Task

class UserCRUDTests(TestCase):
    def setUp(self):
        # Создаем пользователя для тестирования
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user.save()

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
    

class TaskCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.status = Status.objects.create(name='New')

    def test_task_create(self):
        response = self.client.post(reverse('task-create'), {
            'name': 'New Task',
            'description': 'Task description',
            'status': self.status.id,
            'assigned_to': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update(self):
        task = Task.objects.create(name='Old Task', description='Old description', status=self.status, author=self.user)
        response = self.client.post(reverse('task-update', args=[task.id]), {
            'name': 'Updated Task',
            'description': 'Updated description',
            'status': self.status.id,
            'assigned_to': self.user.id
        })
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertEqual(task.name, 'Updated Task')

    def test_task_delete(self):
        task = Task.objects.create(name='Task to delete', description='Description', status=self.status, author=self.user)
        response = self.client.post(reverse('task-delete', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='Task to delete').exists())