# Generated by Django 5.0.6 on 2024-09-10 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("job_seekers", "0016_alter_jobseeker_user_permissions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jobseeker",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to.",
                related_name="job_seeker_groups",
                related_query_name="job_seeker",
                to="auth.group",
            ),
        ),
    ]