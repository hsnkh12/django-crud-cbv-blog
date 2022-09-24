from django.urls import path
from .views import TodoCreateView, TodoDeleteView, TodoListView, TodoUpdateView
from django.views.generic import TemplateView

app_name = 'todos'

urlpatterns = [
    path('',TemplateView.as_view(template_name='home.html'),name='home'),
    path('tasks/',TodoListView.as_view(), name='tasks'),
    path('tasks-create/',TodoCreateView.as_view(),name='tasks-create'),
    path('tasks-update/<pk>',TodoUpdateView.as_view(),name='tasks-update'),
    path('tasks-delete/<pk>',TodoDeleteView.as_view(),name='tasks-delete')
]