# Generated by Django 3.2 on 2021-04-07 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctors', '0003_rename_speciality_doctor_specialty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
