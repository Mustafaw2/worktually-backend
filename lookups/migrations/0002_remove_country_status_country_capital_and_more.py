# Generated by Django 5.0.6 on 2024-06-20 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lookups", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="country",
            name="status",
        ),
        migrations.AddField(
            model_name="country",
            name="capital",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="country",
            name="currency",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="country",
            name="iso2",
            field=models.CharField(default="", max_length=2),
        ),
        migrations.AddField(
            model_name="country",
            name="iso3",
            field=models.CharField(default="", max_length=3),
        ),
        migrations.AddField(
            model_name="country",
            name="phone_code",
            field=models.CharField(default="", max_length=20),
        ),
        migrations.AlterField(
            model_name="country",
            name="name",
            field=models.CharField(default="", max_length=100),
        ),
    ]