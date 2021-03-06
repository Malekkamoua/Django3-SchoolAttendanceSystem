# Generated by Django 3.0.7 on 2020-06-05 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('levels', '__first__'),
        ('courses', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cin', models.IntegerField()),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('phone', models.IntegerField(default='711111111')),
                ('email', models.CharField(default='student@mail.com', max_length=255)),
                ('profile_pic', models.ImageField(default='no_image.png', upload_to='')),
                ('class_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='levels.Class_uni')),
            ],
        ),
        migrations.CreateModel(
            name='Elimination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_absences', models.IntegerField()),
                ('eliminated', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='students.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('present', models.BooleanField(default=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='levels.Class_uni')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.Student')),
            ],
        ),
    ]
