from django.urls import path
from .views import StatusListView, StatusCreateView, StatusUpdateView, StatusDeleteView

urlpatterns = [
    path('', StatusListView.as_view(), name='status-list'),
    path('create/', StatusCreateView.as_view(), name='status-create'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='status-update'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='status-delete'),
]