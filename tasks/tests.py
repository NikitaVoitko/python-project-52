from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from statuses.models import Status
from .models import Task
from labels.models import Label


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


class TaskFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.status = Status.objects.create(name='In Progress')
        self.label = Label.objects.create(name='Bug')
        self.task1 = Task.objects.create(name='Task 1', description='Description 1', status=self.status, author=self.user)
        self.task2 = Task.objects.create(name='Task 2', description='Description 2', status=self.status, author=self.user)
        self.task2.labels.add(self.label)

    def test_filter_by_status(self):
        response = self.client.get(reverse('task-list'), {'status': self.status.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')

    def test_filter_by_label(self):
        response = self.client.get(reverse('task-list'), {'labels': self.label.id})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')

    def test_filter_by_author(self):
        response = self.client.get(reverse('task-list'), {'author': self.user.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task 1')
        self.assertContains(response, 'Task 2')