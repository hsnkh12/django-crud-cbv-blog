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

