# Generated by Django 4.0 on 2022-01-30 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Dashboard', '0005_alter_student_profile_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Todo_Title', models.CharField(max_length=254)),
                ('Todo_Finished', models.BooleanField(default=False)),
                ('Todo_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'verbose_name': 'Todo',
                'verbose_name_plural': 'Todo',
            },
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Homework_Subject', models.CharField(max_length=50)),
                ('Homework_Title', models.CharField(max_length=100)),
                ('Homework_Description', models.TextField()),
                ('Homework_Due', models.DateTimeField()),
                ('Homework_Finished', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
