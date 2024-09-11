# Generated by Django 5.0.6 on 2024-09-10 07:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("job_seekers", "0013_jobseeker_city_jobseeker_state_and_more"),
        ("lookups", "0007_degreetitle"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="jobseeker",
            options={"ordering": ["last_name", "first_name"]},
        ),
        migrations.RemoveField(
            model_name="jobseeker",
            name="source_id",
        ),
        migrations.AddField(
            model_name="jobseeker",
            name="source",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="lookups.source",
            ),
        ),
        migrations.AlterField(
            model_name="jobseeker",
            name="cover_photo",
            field=models.ImageField(blank=True, null=True, upload_to="cover_photos/"),
        ),
        migrations.AlterField(
            model_name="jobseeker",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
                max_length=45,
            ),
        ),
        migrations.AlterField(
            model_name="jobseeker",
            name="profile_picture",
            field=models.ImageField(
                blank=True, null=True, upload_to="profile_pictures/"
            ),
        ),
        migrations.AlterField(
            model_name="jobseeker",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("active", "Active"), ("inactive", "Inactive")],
                max_length=45,
            ),
        ),
        migrations.AddIndex(
            model_name="jobseeker",
            index=models.Index(fields=["id"], name="job_seekers_id_d4d087_idx"),
        ),
    ]
