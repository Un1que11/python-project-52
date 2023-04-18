# Generated by Django 4.1.6 on 2023-04-17 11:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created date')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]