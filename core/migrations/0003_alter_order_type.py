# Generated by Django 3.2.6 on 2021-08-25 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.IntegerField(choices=[(1, 'BUY'), (2, 'SELL')]),
        ),
    ]
