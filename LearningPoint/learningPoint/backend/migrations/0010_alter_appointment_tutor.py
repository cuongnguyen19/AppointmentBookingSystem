# Generated by Django 3.2 on 2022-11-03 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_alter_appointment_tutor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.tutor'),
        ),
    ]
