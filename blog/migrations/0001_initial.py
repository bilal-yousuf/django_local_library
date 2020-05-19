# Generated by Django 3.0.2 on 2020-05-19 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('body', models.TextField(help_text='What is the body of your blog post?')),
                ('pub_date', models.DateField(auto_now_add=True)),
                ('pub_time', models.TimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, choices=[('b', 'Blog post'), ('n', 'Note')], default='n', help_text='Blog post or note?', max_length=1)),
            ],
            options={
                'ordering': ['-pub_date', '-pub_time'],
            },
        ),
    ]
