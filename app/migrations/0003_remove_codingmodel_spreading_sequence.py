# Generated by Django 5.0.3 on 2024-03-09 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_codingmodel_decode_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codingmodel',
            name='spreading_sequence',
        ),
    ]
