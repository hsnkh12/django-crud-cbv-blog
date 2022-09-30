# Django-CRUD-CBV
This app is built for my blog tutorial -> https://hassanelabdallah.hashnode.dev/build-a-django-crud-app-using-class-based-views


### Part 1: Create a Django project 

1- Create a new directory and move inside it.

```
$ mkdir Todo_app
$ cd Todo_app
``` 

2- Create a new virtual environment and activate it.

```
$ python3 -m venv venv
$ source venv/bin/activate
``` 

3- Install Django.

```
$ pip3 install django
``` 

4- Start new Django project and move inside it.

```
$ django-admin startproject app 
$ cd app
``` 

5- Create new app.

```
$ python3 manage.py startapp todos
``` 

6- Create templates directory.

```
$ mkdir templates
``` 

7- Files structure will be as follows: 

```
"."
|-- "app"
|   |-- "app"
|   |   |-- "__init__.py"
|   |   |-- "asgi.py"
|   |   |-- "settings.py"
|   |   |-- "urls.py"
|   |   `-- "wsgi.py"
|   |-- "manage.py"
|   |-- "templates"
|   `-- "todos"
|       |-- "__init__.py"
|       |-- "admin.py"
|       |-- "apps.py"
|       |-- "migrations"
|       |   `-- "__init__.py"
|       |-- "models.py"
|       |-- "tests.py"
|       `-- "views.py"
`-- "venv"
``` 

### Part 2: Setting up the project

1- Go to **app/app/settings.py** and add todos app to INSTALLED_APPS to use it in the project.

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

		# Add this line 
    'todos'
]
```

2- Go to **app/app/settings.py** and add templates Directory in TEMPLATES DIRS to use html templates in views. 

```
import os
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
				# Add this line
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

3- Apply the migrations to create the tables in the sqlite3 database.

```
$ python3 manage.py migrate
``` 

4- Create super user for admin panel by the following command and add your username and password.

```
$ python3 manage.py createsuperuser
``` 

### Part 3: Define todos app models 

1- Go to **app/todos/models.py** and start adding the database models as shown below:

```
from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse

# Create your models here.
class Task(models.Model):

    todo = models.CharField(
        max_length= 100,
        verbose_name= _('To-Do task')
    )

    completed = models.BooleanField(
        default= False
    )

    timeToComplete = models.TimeField()

    def get_absolute_url(self):
        return reverse('todos:tasks-update', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.todo}'
``` 
You can add more models or fields if you want, but for the sake of simplicity, let's keep it that way.

2- Generate the migrations file, and then apply those changes to the database. 

```
$ python3 manage.py makemigrations 
$ python3 manage.py migrate
``` 
3- Go to **app/todos/admin.py** and register Task model in the admin panel.

```
from django.contrib import admin
from .models import Task

# Register your models here.
admin.site.register(Task)
``` 


### Part 4: Creating routes and views

1- Go to **app/todos** and create urls.py file.

```
$ touch urls.py
``` 

2- Go to **app/app/urls.py** and include todos app urls to urlpatterns.

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Add this line
    path('',include('todos.urls'))
]
```

3- Before we start writing our views, go to **app/todos** and create a forms.py file. So we can add forms and use them to create and update the tasks.

```
$ touch forms.py
``` 
```
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
``` 
```CreateTaskForm``` is for **create task view,** and ```UpdateTaskFrom``` is for **update task view**. The reason for doing that is to give each view access to specific fields.

3- Go to **app/todos/views.py**, and let's start building our **class-based views**.

4- Now let's start with the **Create task feature**. We will use a class called ```CreateView```. It is a generic edit view provided by Django for creating a new object, with a response rendered by a template. 
For more, visit [Classy CBV CreateView](https://ccbv.co.uk/projects/Django/4.0/django.views.generic.edit/CreateView/)

```
from django.views.generic import CreateView
from .models import Task
from .forms import CreateTaskForm

# Create - POST
class TodoCreateView(CreateView):

    model = Task
    form_class = CreateTaskForm
    template_name = 'tasks_create_update.html'
    success_url = '/tasks/'
``` 

5- Next, let's add **Retrieve and update task feature**. We are going to use ```UpdateView```. It is a generic edit view for updating an object, with a response rendered by a template.
For more, visit [Classy CBV UpdateView](https://ccbv.co.uk/projects/Django/4.0/django.views.generic.edit/UpdateView/)

```
from django.urls import reverse
from django.views.generic import UpdateView
from .models import Task
from .forms import UpdateTaskForm

# Retrieve,Update - GET,POST
class TodoUpdateView(UpdateView):

    model = Task
    form_class = UpdateTaskForm
    template_name = 'tasks_create_update.html'
    
    def get_success_url(self) -> str:
        taskPK = self.kwargs.get('pk')
        return reverse('todos:tasks-update', kwargs={'pk':taskPK})
``` 
It is pretty similar to ```CreateView```, The only difference here is that it's returning back 
"/tasks-update/{pk}" as a success URL, by adding task's primary key to the URL as a keyword argument using ```reverse function```. This step is optional, you can return any success URL that suits your app, or you can keep it as ```success_url = '/tasks/'```.


6- Next, let's add **Task list feature**. We are going to use ```ListView```, It's a generic list view that renders some list of objects. 
For more, visit [Classy CBV ListView](https://ccbv.co.uk/projects/Django/4.0/django.views.generic.list/ListView/)

```
from django.views.generic import ListView
from .models import Task

# List - GET
class TodoListView(ListView):

    model = Task
    template_name = 'index.html'
    context_object_name = 'tasks'
``` 
```context_object_name``` Is the same as saying ```context = {'tasks':queryset}``` in function based views. By default it will be ```context_object_name="objects"```.

7- Now let's add our last view, which is **Delete task feature**. We are going to use ```DeleteView```, it's a generic edit view for deleting an object retrieved.
For more, visit [Classy CBV DeleteView](https://ccbv.co.uk/projects/Django/4.0/django.views.generic.edit/DeleteView/)

```
from django.views.generic import DeleteView
from .models import Task

# Delete - GET,DELETE
class TodoDeleteView(DeleteView):

    model = Task
    success_url = '/tasks/'
    template_name = 'task_confirm_delete.html'
``` 
HTML template here will act as a delete confirmation page. You can define it in the class, or we can just create "task_confirm_delete.html" file and it will locate it by default.

8- overall view of **app/todos/views.py** file will be as follows:

```
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
``` 

9- Now for the last step in this part, let's add our URL patterns. Go to **app/todos/urls.py** and add the following:

```
from django.urls import path
from .views import TodoCreateView, TodoDeleteView, TodoListView, TodoUpdateView

app_name = 'todos'

urlpatterns = [
    path('tasks/',TodoListView.as_view(), name='tasks'),
    path('tasks-create/',TodoCreateView.as_view(),name='tasks-create'),
    path('tasks-update/<pk>',TodoUpdateView.as_view(),name='tasks-update'),
    path('tasks-delete/<pk>',TodoDeleteView.as_view(),name='tasks-delete')
]
``` 


### Part 5: Creating HTML Templates

1- Now for the final part, let's create our HTML templates to test our views. You can create your own UI and styles, but we are keeping it simple here for you to focus on the CBV concepts.

2- Go to **app/templates** and create the following files:

- base.html
- index.html
- tasks_create_update.html
- task_confirm_delete.html

3- Go to **app/templates/base.html** and add the following:

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>To-Do app</title>
</head>
<body>

    <nav>
        <!-- Add your Navbar here-->
    </nav>
    

    {% block content %}
    {% endblock content %}

    <footer>
        <!-- Add your Footer here-->
    </footer>
    
</body>
</html>
``` 

4- Go to **app/templates/index.html** and add the following:

```
{% extends "base.html" %}

{% block content %}

    <h1>Tasks</h1>
    <a href="{% url 'todos:tasks-create' %}">Create task</a>

    {% for task in tasks %}
    
        <div>
            {% if task.completed %}
            <strike>{{task.todo}}</strike>
            {% else %}
            <p>{{task.todo}}</p>
            {% endif %}
            <a href="{{task.get_absolute_url}}">Edit</a>
            <a href="{% url 'todos:tasks-delete' pk=task.pk %}">Delete</a>
        </div>

        <hr>

    {% endfor %}

{% endblock content %}
``` 

5- Go to **app/templates/tasks_create_update.html** and add the following:

```
{% extends "base.html" %}

{% block content %}

    <form method="POST">
        {% csrf_token %}
        {{ form.as_p}}
        <button type="submit">Confirm</button>
        <a href="{% url 'todos:tasks'%}">Get back</a>
    </form>

{% endblock content %}
``` 

6- And for the last step, go to **app/templates/task_confirm_delete.html** and add the following:

```
{% extends "base.html" %}

{% block content %}

<form method="post">{% csrf_token %}
    <p>Are you sure you want to delete "{{ object }}"?</p>
    <input type="submit" value="Confirm">
    <a href="{% url 'todos:tasks' %}">Cancel</a>
</form>

{% endblock content %}
``` 

That's it! Now run the server, and go to ```localhost:8000/tasks``` URL.

```
$ python3 manage.py runserver
```
and now you have a functional CRUD To-Do app using CBV.
