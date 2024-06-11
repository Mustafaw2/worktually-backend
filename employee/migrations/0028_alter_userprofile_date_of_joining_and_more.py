from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee", "0027_alter_bankaccount_account_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="date_of_joining",
            field=models.DateField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="employee_type",
            field=models.CharField(default="", max_length=50),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="source_of_hiring",
            field=models.CharField(default="", max_length=100),
        ),
    ]

