# Generated by Django 3.1.2 on 2020-11-03 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='id',
            field=models.CharField(editable=False, max_length=40, primary_key=True, serialize=False),
        ),
    ]
