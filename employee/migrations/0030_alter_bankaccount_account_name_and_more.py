# Generated by Django 5.0.6 on 2024-06-05 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0029_alter_userprofile_date_of_joining_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bankaccount",
            name="account_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="bankaccount",
            name="bank_currency",
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name="bankaccount",
            name="bank_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="bankaccount",
            name="iban",
            field=models.CharField(blank=True, max_length=34, null=True),
        ),
    ]