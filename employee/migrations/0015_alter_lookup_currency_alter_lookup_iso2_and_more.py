# Generated by Django 5.0.6 on 2024-05-27 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0014_lookup_capital_lookup_currency_lookup_iso2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lookup',
            name='currency',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='lookup',
            name='iso2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookup',
            name='iso3',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='lookup',
            name='phone_code',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]