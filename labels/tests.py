from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from statuses.models import Status
from tasks.models import Task
from .models import Label

User = get_user_model()

class LabelCRUDTests(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='testuser')
        self.client.force_login(self.user)  # Явно авторизуем пользователя
        self.status = Status.objects.get(name='New')
        self.label = Label.objects.get(name="Bug")
        self.task = Task.objects.get(name="Test task 1")
        self.task.labels.add(self.label)

    def test_label_list_view(self):
        response = self.client.get(reverse('label-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_label_create_view(self):
        response = self.client.post(reverse('label-create'), {'name': 'New Feature'})
        self.assertEqual(response.status_code, 302)  # Ожидание редиректа
        self.assertTrue(Label.objects.filter(name='New Feature').exists())

    def test_label_update_view(self):
        response = self.client.post(reverse('label-update', args=[self.label.id]), {'name': 'Bug Updated'})
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Bug Updated')

    def test_label_delete_view_protected(self):
        response = self.client.post(reverse('label-delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 302)  # Проверка на редирект
        self.assertRedirects(response, reverse('label-list'))  # Проверка, что редирект ведет на список меток
        self.assertTrue(Label.objects.filter(name='Bug').exists())  # Убедимся, что метка все еще существует

    def test_label_delete_view_allowed(self):
        self.task.labels.remove(self.label)
        response = self.client.post(reverse('label-delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(name='Bug').exists())