from django.forms import ModelForm
from .models import Task

# Add your forms here
class CreateTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ['todo', 'timeToComplete']

class UpdateTaskForm(ModelForm):

    class Meta:
        model = Task
        fields = '__all__'