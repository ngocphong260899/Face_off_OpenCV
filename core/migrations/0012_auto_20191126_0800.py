# Generated by Django 2.2.5 on 2019-11-26 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20191126_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roll_up',
            name='date',
            field=models.DateField(),
        ),
    ]