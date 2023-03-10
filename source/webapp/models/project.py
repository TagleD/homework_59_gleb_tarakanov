from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Название')
    description = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Описание')
    started_at = models.DateField(verbose_name='Время создания', null=False)
    ended_at = models.DateField(null=True, default=None, verbose_name='Время завершения')

    def __str__(self):
        return f'{self.name}'
