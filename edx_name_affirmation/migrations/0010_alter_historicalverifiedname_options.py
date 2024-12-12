# Generated by Django 4.2.16 on 2024-10-07 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edx_name_affirmation', '0009_add_verifiedname_platform_verification_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='historicalverifiedname',
            options={'get_latest_by': ('history_date', 'history_id'), 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical verified name', 'verbose_name_plural': 'historical verified names'},
        ),
    ]
