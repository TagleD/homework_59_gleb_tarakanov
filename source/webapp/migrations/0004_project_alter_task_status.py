# Generated by Django 4.1.6 on 2023-03-10 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_alter_task_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.TextField(max_length=3000, verbose_name='Описание')),
                ('started_at', models.DateField(verbose_name='Время создания')),
                ('ended_at', models.DateField(default=None, null=True, verbose_name='Время завершения')),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='statuses', to='webapp.status', verbose_name='Статус'),
        ),
    ]
