# Generated by Django 3.0.7 on 2020-06-27 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20200626_2223'),
        ('students', '0003_remove_attendance_image_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance_image',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='authentication.UserProfile'),
            preserve_default=False,
        ),
    ]
