# Generated by Django 5.0.4 on 2024-04-26 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('set_is_active', 'can change is_active')]},
        ),
    ]