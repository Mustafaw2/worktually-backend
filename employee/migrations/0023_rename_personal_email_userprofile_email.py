# Generated by Django 5.0.6 on 2024-05-31 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0022_userprofile_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='personal_email',
            new_name='email',
        ),
    ]