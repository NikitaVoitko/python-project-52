from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from task_manager.apps.users.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.apps.users.urls')),
    path('statuses/', include('task_manager.apps.statuses.urls')),
    path('tasks/', include('task_manager.apps.tasks.urls')),
    path('labels/', include('task_manager.apps.labels.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
