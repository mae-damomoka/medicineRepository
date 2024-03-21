# Generated by Django 5.0.1 on 2024-02-13 10:20

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_event'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='end_datetime',
            new_name='start_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='start_datetime',
        ),
        migrations.AddField(
            model_name='event',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.CreateModel(
            name='AnotherModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.event')),
            ],
        ),
    ]
