# Generated by Django 3.1.2 on 2020-10-31 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0002_auto_20201031_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='current_goal',
            field=models.TextField(default='testing'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='target_carbs',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='target_fat',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='target_protein',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
    ]
