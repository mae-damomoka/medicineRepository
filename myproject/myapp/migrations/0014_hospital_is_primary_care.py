# Generated by Django 5.0.1 on 2024-02-09 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_remove_hospital_departments_hospital_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='is_primary_care',
            field=models.BooleanField(default=False),
        ),
    ]
