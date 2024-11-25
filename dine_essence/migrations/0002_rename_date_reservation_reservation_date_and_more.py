# Generated by Django 4.2.16 on 2024-11-25 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dine_essence', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='date',
            new_name='reservation_date',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='time',
            new_name='reservation_time',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='name',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='table',
        ),
        migrations.AddField(
            model_name='reservation',
            name='first_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='reservation',
            name='last_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='guests',
            field=models.PositiveIntegerField(),
        ),
    ]
