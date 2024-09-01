from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from statuses.models import Status  # Импорт модели Status из приложения statuses
from tasks.models import Task
from .models import Label

User = get_user_model()

class LabelCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.status = Status.objects.create(name='New')
        self.label = Label.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Test Task",
            description="Task Description",
            status=self.status,
            author=self.user
        )
        self.task.labels.add(self.label)

    def test_label_list_view(self):
        response = self.client.get(reverse('label-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_label_create_view(self):
        response = self.client.post(reverse('label-create'), {'name': 'Feature'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Feature').exists())

    def test_label_update_view(self):
        response = self.client.post(reverse('label-update', args=[self.label.id]), {'name': 'Bug Updated'})
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Bug Updated')

    def test_label_delete_view_protected(self):
        response = self.client.post(reverse('label-delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 200)  # Статус-код должен быть 200, возвращаемся на ту же страницу
        self.assertTrue(Label.objects.filter(name='Bug').exists())  # Метка все еще существует

    def test_label_delete_view_allowed(self):
        self.task.labels.remove(self.label)  # Убираем метку из задачи, чтобы тестировать удаление
        response = self.client.post(reverse('label-delete', args=[self.label.id]))
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после удаления
        self.assertFalse(Label.objects.filter(name='Bug').exists())  # Проверка, что метка удалена