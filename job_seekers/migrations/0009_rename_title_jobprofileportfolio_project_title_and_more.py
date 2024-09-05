# Generated by Django 5.0.6 on 2024-09-04 12:02

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job_seekers", "0008_language_created_at_language_updated_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="jobprofileportfolio",
            old_name="title",
            new_name="project_title",
        ),
        migrations.RemoveField(
            model_name="jobprofileportfolio",
            name="tags",
        ),
        migrations.AddField(
            model_name="jobprofileportfolio",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="jobprofileportfolio",
            name="updated_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="jobprofileportfolio",
            name="files",
            field=models.FileField(upload_to="portfolios/"),
        ),
    ]
