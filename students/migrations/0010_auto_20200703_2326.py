# Generated by Django 3.0.7 on 2020-07-03 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_auto_20200703_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance_detail',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='attendance_image',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
