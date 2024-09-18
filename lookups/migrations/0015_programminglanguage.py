# Generated by Django 5.0.6 on 2024-09-16 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lookups", "0014_frameworks"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProgrammingLanguage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="programming_languages",
                        to="lookups.skillcategory",
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(fields=["id"], name="lookups_pro_id_ca02e7_idx")
                ],
            },
        ),
    ]
