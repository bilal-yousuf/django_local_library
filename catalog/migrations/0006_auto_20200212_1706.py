# Generated by Django 3.0.2 on 2020-02-12 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_blogpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='pub_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
