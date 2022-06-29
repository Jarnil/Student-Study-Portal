# Generated by Django 4.0 on 2022-01-25 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student_Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Display_Name', models.CharField(blank=True, max_length=256)),
                ('Student_Branch', models.CharField(blank=True, max_length=256)),
                ('Student_Semester', models.IntegerField(blank=True)),
                ('Student_Profile_Photo', models.ImageField(blank=True, upload_to='profilePics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
