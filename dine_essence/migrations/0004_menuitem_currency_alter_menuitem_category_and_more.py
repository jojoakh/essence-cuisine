# Generated by Django 4.2.16 on 2024-11-25 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dine_essence', '0003_menuitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='currency',
            field=models.CharField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')], default='USD', max_length=3),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='category',
            field=models.CharField(choices=[('starter', 'Starter'), ('main', 'Main Course'), ('dessert', 'Dessert')], max_length=20),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]