# Generated by Django 3.1.2 on 2020-10-31 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0005_auto_20201031_0636'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='current_goal',
        ),
        migrations.AddField(
            model_name='user',
            name='current_goals',
            field=models.CharField(default='this is a test', max_length=200),
            preserve_default=False,
        ),
    ]
