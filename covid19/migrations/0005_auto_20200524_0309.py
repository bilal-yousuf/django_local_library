# Generated by Django 3.0.2 on 2020-05-24 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid19', '0004_auto_20200524_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='confirmed_cases',
            field=models.CharField(blank=True, default=None, help_text='Total number of confirmed cases in a given day.', max_length=20, null=True, verbose_name='Confirmed Cases'),
        ),
    ]