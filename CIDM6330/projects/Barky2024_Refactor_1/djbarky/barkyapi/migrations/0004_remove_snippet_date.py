# Generated by Django 5.0.1 on 2024-04-21 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barkyapi', '0003_snippet_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='date',
        ),
    ]
