# Generated by Django 2.2.24 on 2021-08-16 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edx_name_affirmation', '0003_verifiedname_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifiedname',
            name='is_verified',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
