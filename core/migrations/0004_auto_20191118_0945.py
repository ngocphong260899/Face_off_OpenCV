# Generated by Django 2.2.5 on 2019-11-18 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20191118_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roll_up',
            name='date',
            field=models.DateField(),
        ),
    ]