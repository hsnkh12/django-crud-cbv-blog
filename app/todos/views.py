from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from .models import Task
from .forms import CreateTaskForm, UpdateTaskForm

# Create - POST
class TodoCreateView(CreateView):

    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks_create_update.html'
    success_url = '/tasks/'

# Retrieve,Update - GET,POST
class TodoUpdateView(UpdateView):

    model = Task
    form_class = UpdateTaskForm
    template_name = 'tasks_create_update.html'
    
    def get_success_url(self) -> str:
        taskPK = self.kwargs.get('pk')
        return reverse('todos:tasks-update', kwargs={'pk':taskPK})

# List - GET
class TodoListView(ListView):

    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'

# Delete - GET,DELETE
class TodoDeleteView(DeleteView):

    model = Task
    success_url = '/tasks/'
    template_name = 'task_confirm_delete.html'