from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from statuses.models import Status
from .models import Task
from labels.models import Label

User = get_user_model()
class TaskCRUDTests(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='testuser')
        self.client.force_login(self.user)  # Авторизуем пользователя
        self.status = Status.objects.get(name='New')

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
        task = Task.objects.get(name='Test task 1')
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
        task = Task.objects.get(name='Test task 2')
        response = self.client.post(reverse('task-delete', args=[task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(name='Test task 2').exists())

class TaskFilterTests(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='testuser')
        self.client.force_login(self.user)  # Авторизуем пользователя
        self.status = Status.objects.get(name='In Progress')
        self.label = Label.objects.get(name='Bug')

    def test_filter_by_status(self):
        response = self.client.get(reverse('task-list'), {'status': self.status.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test task 3')

    def test_filter_by_label(self):
        task = Task.objects.get(name="Test task 1")
        task.labels.add(self.label)
        response = self.client.get(reverse('task-list'), {'labels': self.label.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test task 1')
        self.assertNotContains(response, 'Test task 2')

    def test_filter_by_author(self):
        response = self.client.get(reverse('task-list'), {'author': self.user.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test task 1')
        self.assertContains(response, 'Test task 2')